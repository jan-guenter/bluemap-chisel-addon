/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chisel.adapter.bluemap522;

import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.chisel.activation.ChiselRuntime;

/** Resource-pack extension factory registered before resource loading begins. */
final class ChiselResourceExtensionType
        implements ResourcePack.Extension<ChiselResourceExtension> {

    static final Key KEY = Key.parse("bluemap_chisel:exact_profile");

    private final ChiselRuntime runtime;

    ChiselResourceExtensionType(ChiselRuntime runtime) {
        this.runtime = runtime;
    }

    @Override
    public Key getKey() {
        return KEY;
    }

    @Override
    public ChiselResourceExtension create(ResourcePack pack) {
        return new ChiselResourceExtension(pack, runtime);
    }
}
