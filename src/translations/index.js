import Vue from 'vue'
import GetTextPlugin from 'vue-gettext'

// Default translations to english language
import translations from '@/translations/en.json'

Vue.use(GetTextPlugin, {
    availableLanguages: {
        en: 'English',
        de: 'Deutsch'
    },
    defaultLanguage: 'en',
    languageVmMixin: {
        methods: {
            merge(locale) {
                Object.assign(translations, locale);
            },
        }
    },
    translations: translations,
    silent: true,
})