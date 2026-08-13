/* SPDX-License-Identifier: MIT */
package io.github.janguenter.bluemap.chisel.adapter.bluemap522;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.janguenter.bluemap.chisel.profile.LoaderFamily;
import org.junit.jupiter.api.Test;

class ChiselRendererMappingTest {

    @Test
    void onlyCtmPerformsExactNativeIdInternalFaceSuppression() {
        assertTrue(ChiselRenderer.earlySuppressesInternalFace(LoaderFamily.CTM));
        assertFalse(ChiselRenderer.earlySuppressesInternalFace(LoaderFamily.GIANT));
    }

    @Test
    void registryAndSyntheticIdsCannotCollideWithChippedAddon() {
        assertEquals("bluemap_chisel:athena_shape",
                BlueMap522Adapter.RENDERER_KEY.getFormatted());
        assertEquals(BlueMap522Adapter.RENDERER_KEY, ChiselResourceExtension.SYNTHETIC);
        assertEquals("bluemap_chisel:exact_profile",
                ChiselResourceExtensionType.KEY.getFormatted());
        assertFalse(BlueMap522Adapter.RENDERER_KEY.getFormatted()
                .startsWith("bluemap_chipped:"));
        assertFalse(ChiselResourceExtensionType.KEY.getFormatted()
                .startsWith("bluemap_chipped:"));
    }
}
