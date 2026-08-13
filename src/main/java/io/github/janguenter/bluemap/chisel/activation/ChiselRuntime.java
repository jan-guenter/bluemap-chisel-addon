/*
 * SPDX-License-Identifier: MIT
 */
package io.github.janguenter.bluemap.chisel.activation;

/** Process-scoped state for the single exact Chisel/Athena route. */
public final class ChiselRuntime {

    public static final String ROUTE_ID = "chisel-athena-2.0.1-4.0.6";
    public static final ChiselRuntime INSTANCE = new ChiselRuntime();

    private final RouteActivation route = new RouteActivation(ROUTE_ID);

    private ChiselRuntime() {
    }

    public RouteActivation route() {
        return route;
    }

    public void disable(String detail) {
        route.fail(detail);
    }
}
