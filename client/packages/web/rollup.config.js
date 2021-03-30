import Vue from "rollup-plugin-vue"
import path from "path"
import serve from "rollup-plugin-serve"

const dev = process.env.DEV === "true"

export default {
    input: path.resolve(__dirname, "src/index.js"),
    output: {
        name: "index.js",
        format: "amd",
        dir: "dist"
    },
    plugins: [
        Vue(),
        dev && serve({
            contentBase: ["dist"],
            port: 8082
        }),
    ]
}
