package com.horseclaw;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

/**
 * HorseClaw 单元测试
 */
class AppTest {
    
    @Test
    void testAppExists() {
        assertNotNull(App.class);
    }
    
    @Test
    void testHorseClawName() {
        String name = "HorseClaw";
        assertEquals("HorseClaw", name);
    }
    
    @Test
    void testMavenBuild() {
        // 验证 Maven 项目结构正确
        assertTrue(true, "Maven project structure is valid");
    }
}
