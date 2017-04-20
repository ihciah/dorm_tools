<?php
require '../wechat-php-sdk/autoload.php';

use Gaoming13\WechatPhpSdk\Wechat;

$wechat = new Wechat(array( 
    'appId'         =>  'aaaaa',   
    'token'         =>  'bbbbbb' 
    #'encodingAESKey' => 'cccccc'
));

$BASE_URI = 'http://your_domain/forward.php?time=%s&sign=%s';
$OPEN_DOOR_MSG = array('开门', '开', 'door', 'open', '0');
$AUTHORIZED_USERS = array('id_1', 'id_2', 'id_3', 'id_4');
$KEY = "your_long_key";

function sign_me($s){
    global $KEY;
    return sha1(str_repeat($s, 6) . $KEY);
}

function valid_me($username, $create_time){
    global $AUTHORIZED_USERS, $BASE_URI;
    if (in_array($username, $AUTHORIZED_USERS)){
        if (trim(file_get_contents(sprintf($BASE_URI, $create_time, sign_me($create_time)))) == 'OK'){
            return 0;
        }
        return -2;
    }
    return -1;
}

$msg = $wechat->serve();
if ($msg->MsgType == 'text' && $msg->Content == '你好') {
    $wechat->reply("Hello!");
}
else if ($msg->MsgType == 'text' && $msg->Content == 'id' || $msg->Content == 'whoami') {
    $wechat->reply(strval($msg->FromUserName));
}
else if ($msg->MsgType == 'text' && $msg->Content == 'time') {
    $wechat->reply(strval($msg->CreateTime));
}
else if ($msg->MsgType == 'text' && in_array($msg->Content, $OPEN_DOOR_MSG)) {
    $ret = valid_me(strval($msg->FromUserName), strval($msg->CreateTime));
    if ($ret == 0)
        $wechat->reply("Door opened.");
    else if ($ret == -1)
        $wechat->reply("Not authorized.");
    else
        $wechat->reply("Unknown error.");
}
else {
    $wechat->reply($msg->Content);
}
