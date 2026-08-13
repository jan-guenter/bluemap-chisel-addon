/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chisel.profile;

import de.bluecolored.bluemap.core.util.Key;

import java.util.Map;
import java.util.Set;
import java.util.stream.Collectors;

/** Exact All the Mons 1.2.0 Chisel/Athena profile. */
public final class Chisel201Athena406Profile {

    public static final String PROFILE_ID = "chisel-athena-2.0.1-4.0.6";
    public static final String CHISEL_SHA256 =
            "66ae1f65374a7409af069d5ccde63a338d1754494555b3b5a00f1e862e50e2a6";
    public static final long CHISEL_SIZE = 8_268_524L;
    public static final String ATHENA_SHA256 =
            "43699885bbce3343916d4c5c4940cf0e3f9f6f02fdeb46e8655e121b42282ec5";
    public static final long ATHENA_SIZE = 99_944L;
    public static final int ALL_CHISEL_BLOCK_COUNT = 1_293;
    public static final int ROUTED_BLOCK_COUNT = 439;
    public static final int CTM_BLOCK_COUNT = 306;
    public static final int GIANT_BLOCK_COUNT = 133;
    public static final int STOCK_BLOCK_COUNT = 854;
    public static final int STOCK_WEIGHTED_VARIANT_COUNT = 117;
    public static final int REQUIRED_TEXTURE_COUNT = 2_195;
    public static final int REQUIRED_RESOURCE_PATH_COUNT = 3_379;
    public static final int REQUIRED_PNG_COUNT = 2_501;
    public static final String DEFINITIONS_SHA256 =
            "3756446dc0559237732576286e9ee490b3e2bae063f2a9d6c4a22a7b1b363669";

    public static final DefinitionCatalog CATALOG = DefinitionCatalog.load(
            "/bluemap-chisel/profiles/chisel/2.0.1-athena-4.0.6/definitions.tsv",
            ROUTED_BLOCK_COUNT,
            DEFINITIONS_SHA256
    );
    public static final Map<String, ChiselDefinition> DEFINITIONS = CATALOG.definitions();
    public static final Set<String> ROUTED_BLOCKS = DEFINITIONS.keySet();
    public static final Set<Key> REQUIRED_TEXTURES = CATALOG.textureIds().stream()
            .map(Key::parse)
            .collect(Collectors.toUnmodifiableSet());
    public static final Set<Key> STATIC_FIRST_FRAME_TEXTURES = Set.of(
            Key.parse("chisel:block/ctm/log_bordered/crimson_planks/0"),
            Key.parse("chisel:block/ctm/log_bordered/crimson_planks/2"),
            Key.parse("chisel:block/ctm/log_bordered/crimson_planks/3"),
            Key.parse("chisel:block/ctm/log_bordered/crimson_planks/4"),
            Key.parse("chisel:block/log_bordered/crimson_planks")
    );

    static {
        if (REQUIRED_TEXTURES.size() != REQUIRED_TEXTURE_COUNT) {
            throw new IllegalStateException("required texture roster changed");
        }
    }

    private Chisel201Athena406Profile() {
    }
}
