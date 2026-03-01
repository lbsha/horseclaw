#!/usr/bin/env python3
"""
AI 驱动开发流水线主程序
集成 MiniMax API 进行代码修复
"""

import os
import sys
import time
import json
import subprocess
from datetime import datetime
from dataclasses import dataclass
from typing import List, Optional

# 导入 MiniMax 客户端
try:
    from minimax_client import call_minimax, fix_code, review_code, explain_error
    MINIMAX_AVAILABLE = True
except ImportError:
    MINIMAX_AVAILABLE = False
    print("⚠️ MiniMax 客户端未找到，将使用占位符")


@dataclass
class Config:
    max_iterations: int = 1000
    iteration_timeout: int = 120
    auto_commit: bool = True
    commit_threshold: int = 3
    max_retries: int = 5
    max_commits_per_hour: int = 50
    
    # MiniMax 配置
    model: str = "MiniMax-M2.1"
    temperature: float = 0.7
    
config = Config()


class AIPipeline:
    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.iteration = 0
        self.success_streak = 0
        self.total_commits = 0
        self.commits_today = 0
        
    def run(self):
        """主循环"""
        print(f"🚀 启动 AI 开发流水线")
        print(f"📁 仓库: {self.repo_path}")
        print(f"🤖 MiniMax: {'已启用' if MINIMAX_AVAILABLE else '未启用'}")
        
        while self.iteration < config.max_iterations:
            self.iteration += 1
            start_time = time.time()
            
            print(f"\n{'='*50}")
            print(f"🔄 循环 #{self.iteration} | 成功 streak: {self.success_streak}")
            print(f"{'='*50}")
            
            # 1. 发现问题
            issues = self.find_issues()
            if not issues:
                print("✅ 未发现问题，休息10秒...")
                time.sleep(10)
                continue
            
            print(f"🔍 发现 {len(issues)} 个问题:")
            for issue in issues:
                print(f"   - {issue}")
            
            # 2. 用 MiniMax 生成修复
            fix_code_result = self.generate_fix_with_minimax(issues)
            if not fix_code_result:
                print("❌ 无法生成修复代码")
                continue
            
            # 3. 审查修复
            review = self.review_fix(fix_code_result)
            print(f"📝 代码审查得分: {review.get('score', 'N/A')}/10")
            
            # 4. 应用修复
            if not self.apply_fix(fix_code_result):
                print("❌ 应用修复失败")
                continue
            
            # 5. 运行测试
            test_result = self.run_tests()
            
            # 6. 决策
            if test_result["passed"]:
                print("✅ 测试通过!")
                self.success_streak += 1
                
                if self.success_streak >= config.commit_threshold:
                    self.auto_commit()
            else:
                print(f"❌ 测试失败: {test_result['error'][:100]}")
                # 用 MiniMax 解释错误
                if MINIMAX_AVAILABLE:
                    explanation = explain_error(test_result["error"])
                    print(f"💡 MiniMax 解释: {explanation[:200]}")
                
                self.success_streak = 0
                
                if self.should_rollback():
                    self.rollback()
            
            # 统计
            elapsed = time.time() - start_time
            print(f"⏱️ 循环耗时: {elapsed:.1f}秒")
        
        print(f"\n📊 统计:")
        print(f"   总循环: {self.iteration}")
        print(f"   总提交: {self.total_commits}")
    
    def find_issues(self) -> List[str]:
        """发现问题"""
        issues = []
        
        # 运行 lint
        lint_result = subprocess.run(
            ["npm", "run", "lint"] if os.path.exists("package.json") 
            else ["npx", "eslint", "."],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            timeout=30
        )
        if lint_result.returncode != 0 and lint_result.stderr:
            issues.append(f"lint: {lint_result.stderr[:200]}")
        
        # 运行测试
        test_result = subprocess.run(
            ["npm", "test", "--", "--passWithNoTests"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            timeout=60
        )
        if test_result.returncode != 0 and test_result.stderr:
            issues.append(f"test: {test_result.stderr[:200]}")
        
        # 运行类型检查
        type_result = subprocess.run(
            ["npx", "tsc", "--noEmit"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            timeout=30
        )
        if type_result.returncode != 0 and type_result.stderr:
            issues.append(f"type: {type_result.stderr[:200]}")
        
        return issues
    
    def generate_fix_with_minimax(self, issues: List[str]) -> Optional[str]:
        """用 MiniMax 生成修复"""
        if not MINIMAX_AVAILABLE:
            print("⚠️ MiniMax 不可用，跳过修复")
            return None
        
        system_prompt = """你是一个高级工程师，擅长修复代码问题。

你的任务是：
1. 分析问题
2. 生成修复代码
3. 只返回代码，不需要解释

要求：
- 使用现代编程风格
- 保持代码简洁
- 确保修复正确"""
        
        prompt = f"""请修复以下问题:

问题列表:
{chr(10).join(f"- {i}" for i in issues)}

请直接给出修复后的代码，不要解释。"""
        
        print("🤖 调用 MiniMax 生成修复...")
        result = call_minimax(
            prompt, 
            system_prompt=system_prompt,
            model=config.model,
            temperature=config.temperature
        )
        
        return result
    
    def review_fix(self, code: str) -> dict:
        """用 MiniMax 审查代码"""
        if not MINIMAX_AVAILABLE:
            return {"score": 10, "issues": []}
        
        return review_code(code)
    
    def apply_fix(self, fix_code: str) -> bool:
        """应用修复"""
        # 创建新分支
        branch_name = f"fix/auto-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        subprocess.run(
            ["git", "checkout", "-b", branch_name],
            cwd=self.repo_path,
            capture_output=True
        )
        
        # 保存修复代码到文件
        # 简化：保存到 FIX.patch
        with open(f"{self.repo_path}/FIX.patch", "w") as f:
            f.write(fix_code)
        
        # 尝试应用
        result = subprocess.run(
            ["git", "apply", "FIX.patch"],
            cwd=self.repo_path,
            capture_output=True
        )
        
        return result.returncode == 0
    
    def run_tests(self) -> dict:
        """运行测试"""
        result = subprocess.run(
            ["npm", "test"],
            capture_output=True,
            text=True,
            cwd=self.repo_path,
            timeout=120
        )
        
        passed = result.returncode == 0
        return {
            "passed": passed,
            "output": result.stdout,
            "error": result.stderr
        }
    
    def should_rollback(self) -> bool:
        """判断是否回滚"""
        return self.success_streak >= config.max_retries
    
    def rollback(self) -> bool:
        """回滚"""
        print("🔙 执行回滚...")
        result = subprocess.run(
            ["git", "checkout", "main"],
            cwd=self.repo_path,
            capture_output=True
        )
        
        # 删除分支
        subprocess.run(
            ["git", "branch", "-D", "fix/auto-*"],
            cwd=self.repo_path,
            shell=True
        )
        
        self.success_streak = 0
        return result.returncode == 0
    
    def auto_commit(self) -> bool:
        """自动提交"""
        if self.commits_today >= config.max_commits_per_hour:
            print("⏸️ 达到每小时提交上限")
            return False
        
        # 添加文件
        subprocess.run(
            ["git", "add", "-A"],
            cwd=self.repo_path,
            capture_output=True
        )
        
        # 提交
        commit_msg = f"🤖 AI修复 #{self.iteration}"
        result = subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=self.repo_path,
            capture_output=True
        )
        
        if result.returncode == 0:
            self.total_commits += 1
            self.commits_today += 1
            self.success_streak = 0
            print(f"✅ 自动提交! 总计: {self.total_commits}")
            
            # 推送
            subprocess.run(
                ["git", "push", "origin", "HEAD"],
                cwd=self.repo_path,
                capture_output=True
            )
            return True
        
        return False


if __name__ == "__main__":
    repo = sys.argv[1] if len(sys.argv) > 1 else "."
    pipeline = AIPipeline(repo)
    pipeline.run()
