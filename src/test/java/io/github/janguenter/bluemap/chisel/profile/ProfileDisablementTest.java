/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chisel.profile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.Set;
import org.junit.jupiter.api.Test;

class ProfileDisablementTest {

    @Test
    void propertyAndEnvironmentValuesMergeCanonically() {
        ProfileDisablement disabled = ProfileDisablement.from(
                " Chisel-Athena-2.0.1-4.0.6,INVALID VALUE ",
                "future,chisel-athena-2.0.1-4.0.6"
        );
        assertEquals(
                Set.of("chisel-athena-2.0.1-4.0.6", "future"),
                disabled.disabledProfiles()
        );
        assertTrue(disabled.isDisabled("CHISEL-ATHENA-2.0.1-4.0.6"));
        assertFalse(disabled.isDisabled("missing"));
    }
}
