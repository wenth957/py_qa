class Chatbox {
    constructor() {
        this.args = {
            // 最下边那个微信图标
            openButton: document.querySelector('.chatbox__button'),
            // 整个聊天机器人
            chatBox: document.querySelector('.chatbox__support'),
            // 发送图标
            sendButton: document.querySelector('.send__button')
        }

        this.state = false;
        this.messages = [];
    }

    display() {
        const {openButton, chatBox, sendButton} = this.args;
        // 他们点击后共同点是：对chatBox元素做相应修改
        // 图标点击后逻辑，负责对话框消失或出现
        openButton.addEventListener('click', () => this.toggleState(chatBox))
        // 发送图标点击后逻辑
        sendButton.addEventListener('click', () => this.onSendButton(chatBox))

        // 除了点击发送，如果按键为回车，也实行onSendButton逻辑
        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox)
            }
        })
    }

    toggleState(chatbox) {
        this.state = !this.state;

        // show or hides the box，增加或者去除这个类，为了让聊天机器人本体消失或者出现
        if(this.state) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        let msg1 = { name: "User", message: text1 }
        this.messages.push(msg1);
        // 这个messages是个数组，定义在最前边，储存输入的句子

        fetch('http://127.0.0.1:5000/predict', {
            method: 'POST',
            // 通过post请求将我们询问的句子上传
            body: JSON.stringify({ message: text1 }),
            mode: 'cors',
            headers: {
              'Content-Type': 'application/json'
            },
          })  //r是response缩写。r的生成逻辑要看ap.py  sam是机器人名字，回答由机器人回答
          .then(r => r.json())
          .then(r => {
            let msg2 = { name: "Sam", message: r.answer };
            this.messages.push(msg2);
            this.updateChatText(chatbox)
            textField.value = ''

        }).catch((error) => {
            console.error('Error:', error);
            this.updateChatText(chatbox)
            textField.value = ''
          });
    }

    updateChatText(chatbox) {
        var html = '';
        this.messages.slice().reverse().forEach(function(item, index) {
            if (item.name === "Sam")
            {
                html += '<div class="messages__item messages__item--visitor">' + item.message + '</div>'
            }
            else
            {
                html += '<div class="messages__item messages__item--operator">' + item.message + '</div>'
            }
          });

        const chatmessage = chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html;
    }
}


const chatbox = new Chatbox();
chatbox.display();