/**
 * Created by bot.su on 2017/5/7.
 * 登录界面
 */

cc.Class({
    extends: cc.Component,

    properties: {

    },

    // use this for initialization
    onLoad: function () {
        cc.view.setDesignResolutionSize(1136,720, cc.ResolutionPolicy.EXACT_FIT );

    },


    youkeLogin:function(){
        cc.director.loadScene('MainScene');
    },


    weixinLogin:function(){
        cc.director.loadScene('MainScene');
    },


    // called every frame, uncomment this function to activate update callback
    update: function (dt) {

    },
});
