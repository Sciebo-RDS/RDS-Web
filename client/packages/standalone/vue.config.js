const Dotenv = require('dotenv-webpack');
const envPath = function () {
    return (!process.env.NODE_ENV || (process.env.NODE_ENV === 'development')) ?
        '../../../.env' :
        `../../../.env.${process.env.NODE_ENV}`;
}

const dotenvArgs = {
    expand: true,
    path: envPath()
};

let publicPath = '/';
if (process.env.NODE_ENV === 'production' && !!process.env.VUE_APP_BASE_URL) {
    publicPath = process.env.VUE_APP_BASE_URL;
}

module.exports = {
    publicPath,
    transpileDependencies: [
        'vuetify',
        'vue-oidc-client'
    ],
    filenameHashing: false,
    productionSourceMap: false,
    devServer: {
        proxy: 'http://localhost:8080'
    },
    configureWebpack: {
        plugins: [
            new Dotenv(dotenvArgs)
        ]
    },
    chainWebpack: config => {
        config.optimization.splitChunks(false)
    }
}