'use strict';
class ChatAI {

    constructor(options) {
        let defaults = {
            api_key: '',
            source: 'openai',
            model: 'gpt-3.5-turbo',
            conversations: [],
            selected_conversation: null,
            container: '.chat-ai',
            chat_speed: 30,
            title: 'Untitled',
            max_tokens: 100,
            version: '1.0.0',
            show_tokens: true,
            available_models: ['gpt-4', 'gpt-4-0613', 'gpt-4-32k', 'gpt-4-32k-0613', 'gpt-3.5-turbo', 'gpt-3.5-turbo-0613', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613']
        };
        this.options = Object.assign(defaults, options);
        this.options.container = document.querySelector(this.options.container);
        this.options.container.innerHTML = `
            ${this._sidebarTemplate()}
            <main class="content">               
                ${this._welcomePageTemplate()}
                <form class="message-form">
                    <input type="text" placeholder="Type a message..." required>
                    <button type="submit"><i class="fa-solid fa-paper-plane"></i></button>
                </form>
            </main>
        `;
        let settings = this.getSettings();
        if (settings) {
            this.options = Object.assign(this.options, settings);
        }
        this._eventHandlers();
        this.container.querySelector('.message-form input').focus();
    }

}