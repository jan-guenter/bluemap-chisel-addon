/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chisel.profile;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.EnumMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.zip.ZipEntry;
import java.util.zip.ZipFile;
import org.junit.jupiter.api.Test;

class ChiselProfileTest {

    @Test
    void exactMetadataOnlyCatalogHasClosedTwoFamilyRoster() {
        assertEquals(439, Chisel201Athena406Profile.DEFINITIONS.size());
        assertEquals(2_195, Chisel201Athena406Profile.REQUIRED_TEXTURES.size());
        Map<LoaderFamily, Integer> counts = new EnumMap<>(LoaderFamily.class);
        Chisel201Athena406Profile.DEFINITIONS.values().forEach(
                definition -> counts.merge(definition.family(), 1, Integer::sum)
        );
        assertEquals(Map.of(
                LoaderFamily.CTM, 306,
                LoaderFamily.GIANT, 133
        ), counts);
        assertTrue(Chisel201Athena406Profile.ROUTED_BLOCKS.stream()
                .allMatch(block -> block.startsWith("chisel:")));
    }

    @Test
    void translucentAndAnimatedExactSubsetsAreClosed() {
        Set<String> glass = new HashSet<>();
        Set<String> ice = new HashSet<>();
        Chisel201Athena406Profile.ROUTED_BLOCKS.forEach(block -> {
            if (block.endsWith("/glass")) {
                glass.add(block);
            }
            if (block.endsWith("/ice")) {
                ice.add(block);
            }
        });
        assertEquals(8, glass.size());
        assertEquals(10, ice.size());
        assertEquals(5, Chisel201Athena406Profile.STATIC_FIRST_FRAME_TEXTURES.size());
        assertTrue(Chisel201Athena406Profile.ROUTED_BLOCKS.contains(
                "chisel:log_bordered/crimson_planks"
        ));
        assertFalse(Chisel201Athena406Profile.ROUTED_BLOCKS.contains(
                "chisel:braid/coal_block"
        ));
    }

    @Test
    void exactJarLeavesAllStockAndWeightedVariantsUnrouted() throws IOException {
        String chiselValue = System.getProperty("chiselJar");
        if (chiselValue == null || !Files.isRegularFile(Path.of(chiselValue))) {
            return;
        }
        int all = 0;
        int stock = 0;
        int weightedStock = 0;
        try (ZipFile archive = new ZipFile(chiselValue)) {
            for (ZipEntry entry : java.util.Collections.list(archive.entries())) {
                String name = entry.getName();
                String prefix = "assets/chisel/blockstates/";
                if (entry.isDirectory() || !name.startsWith(prefix) || !name.endsWith(".json")) {
                    continue;
                }
                all++;
                String block = "chisel:" + name.substring(prefix.length(), name.length() - 5);
                if (Chisel201Athena406Profile.ROUTED_BLOCKS.contains(block)) {
                    continue;
                }
                stock++;
                try (InputStreamReader reader = new InputStreamReader(
                        archive.getInputStream(entry), StandardCharsets.UTF_8
                )) {
                    JsonObject root = JsonParser.parseReader(reader).getAsJsonObject();
                    JsonObject variants = root.has("variants")
                            && root.get("variants").isJsonObject()
                            ? root.getAsJsonObject("variants") : new JsonObject();
                    if (variants.entrySet().stream().map(Map.Entry::getValue)
                            .anyMatch(ChiselProfileTest::weightedVariant)) {
                        weightedStock++;
                    }
                }
            }
        }
        assertEquals(Chisel201Athena406Profile.ALL_CHISEL_BLOCK_COUNT, all);
        assertEquals(Chisel201Athena406Profile.STOCK_BLOCK_COUNT, stock);
        assertEquals(
                Chisel201Athena406Profile.STOCK_WEIGHTED_VARIANT_COUNT,
                weightedStock
        );
    }

    private static boolean weightedVariant(JsonElement value) {
        if (value.isJsonArray()) {
            return true;
        }
        if (!value.isJsonObject()) {
            return false;
        }
        JsonElement weight = value.getAsJsonObject().get("weight");
        return weight != null && weight.getAsInt() != 1;
    }
}
