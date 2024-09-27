const { generate } = require('youtube-po-token-generator');

generate().then(tokens => {
    console.log(JSON.stringify(tokens));
}, console.error);
