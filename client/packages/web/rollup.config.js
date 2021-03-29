import Vue from "rollup-plugin-vue"
import path from "path"
import serve from "rollup-plugin-serve"
import json from '@rollup/plugin-json';
import image from '@rollup/plugin-image';
import { nodeResolve } from '@rollup/plugin-node-resolve';
import styles from "rollup-plugin-styles";
import commonjs from '@rollup/plugin-commonjs';

const dev = process.env.DEV === "true"

export default {
    input: path.resolve(__dirname, "src/index.js"),
    output: {
        name: "extension.js",
        format: "amd",
        dir: "dist"
    },
    plugins: [
        Vue(),
        nodeResolve({ browser: true, }),
        commonjs(),
        json(),
        image(),
        styles(),
        dev && serve({
            contentBase: ["dist"],
            port: 8082
        }),
    ]
}
