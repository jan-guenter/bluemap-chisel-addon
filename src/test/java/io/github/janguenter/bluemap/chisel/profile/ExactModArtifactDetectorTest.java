/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chisel.profile;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ExactModArtifactDetectorTest {

    @Test
    void onlyTheExactInstalledPairActivates() {
        String chiselValue = System.getProperty("chiselJar");
        String athenaValue = System.getProperty("athenaJar");
        if (chiselValue == null || athenaValue == null) {
            return;
        }
        Path chisel = Path.of(chiselValue);
        Path athena = Path.of(athenaValue);
        if (!Files.isRegularFile(chisel) || !Files.isRegularFile(athena)) {
            return;
        }
        assertTrue(ExactModArtifactDetector.matchesRequiredPair(List.of(chisel, athena)));
        assertFalse(ExactModArtifactDetector.matchesRequiredPair(List.of(chisel)));
        assertFalse(ExactModArtifactDetector.matches(
                List.of(chisel, athena),
                Map.of(
                        "chisel", new ExactModArtifactDetector.Identity(
                                Chisel201Athena406Profile.CHISEL_SHA256,
                                Chisel201Athena406Profile.CHISEL_SIZE + 1
                        ),
                        "athena", new ExactModArtifactDetector.Identity(
                                Chisel201Athena406Profile.ATHENA_SHA256,
                                Chisel201Athena406Profile.ATHENA_SIZE
                        )
                )
        ));
    }
}
