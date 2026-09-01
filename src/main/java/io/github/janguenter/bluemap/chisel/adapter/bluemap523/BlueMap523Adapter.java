/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chisel.adapter.bluemap523;

import de.bluecolored.bluemap.core.map.hires.block.BlockRendererType;
import de.bluecolored.bluemap.core.resources.pack.resourcepack.ResourcePack;
import de.bluecolored.bluemap.core.util.Key;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.RegistryGuard;
import io.github.janguenter.bluemap.addon.adapter.api.bluemap523.ResourceExtensionType;
import io.github.janguenter.bluemap.chisel.activation.ChiselRuntime;

/** Exact BlueMap 5.23 feature-backport internal ABI boundary. */
public final class BlueMap523Adapter {

    private static final ChiselRuntime RUNTIME = ChiselRuntime.INSTANCE;
    static final Key RENDERER_KEY =
            Key.parse("bluemap_chisel:athena_shape");
    static final Key EXTENSION_KEY = Key.parse("bluemap_chisel:exact_profile");
    private static final BlockRendererType RENDERER = new BlockRendererType.Impl(
            RENDERER_KEY,
            (pack, gallery, settings) -> new ChiselRenderer(pack, gallery, settings, RUNTIME)
    );
    private static final ResourcePack.Extension<ChiselResourceExtension> EXTENSION =
            new ResourceExtensionType<>(
                    EXTENSION_KEY,
                    pack -> new ChiselResourceExtension(pack, RENDERER, RUNTIME)
            );

    private BlueMap523Adapter() {
    }

    public static synchronized boolean install() {
        if (!RegistryGuard.canRegister(BlockRendererType.REGISTRY, RENDERER)
                || !RegistryGuard.canRegister(ResourcePack.Extension.REGISTRY, EXTENSION)) {
            RUNTIME.disable("registry-collision");
            return false;
        }
        if (!RegistryGuard.register(BlockRendererType.REGISTRY, RENDERER)
                || !RegistryGuard.register(ResourcePack.Extension.REGISTRY, EXTENSION)) {
            RUNTIME.disable("registry-collision");
            return false;
        }
        return true;
    }

    static ResourcePack.Extension<ChiselResourceExtension> extensionType() {
        return EXTENSION;
    }
}
