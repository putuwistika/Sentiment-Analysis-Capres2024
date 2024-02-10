css = '''
<style>
.chat-message {
    padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; display: flex
}
.chat-message.user {
    background-color: #2b313e
}
.chat-message.bot {
    background-color: #475063
}
.chat-message .avatar {
  width: 20%;
}
.chat-message .avatar img {
  max-width: 90px;
  max-height: 92px;
  border-radius: 20%;
  object-fit: cover;
}
.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
  color: #fff;
}
'''

bot_template_anis = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://asset.kompas.com/crops/F2ZGFqk92vfeRAZWRvmT3prfoTw=/128x34:1158x720/750x500/data/photo/2023/12/12/65782fa87b527.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

bot_template_prabowo = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://cdn.rri.co.id/berita/1/images/1702357508032-p/jirjctzs5mdcr6x.jpeg" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

bot_template_ganjar = '''
<div class="chat-message bot">
    <div class="avatar">
        <img src="https://asset.kompas.com/crops/yod3aF36WXY29ZKBBtg41kdU_hc=/46x0:1126x720/750x500/data/photo/2023/12/12/65782ee3b696c.png" style="max-height: 78px; max-width: 78px; border-radius: 50%; object-fit: cover;">
    </div>
    <div class="message">{{MSG}}</div>
</div>
'''

user_template = '''
<div class="chat-message user">
    <div class="avatar">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/1/12/User_icon_2.svg/220px-User_icon_2.svg.png">
    </div>    
    <div class="message">{{MSG}}</div>
</div>
'''
