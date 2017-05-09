/**
 * Created by bot.su on 2017/5/7.
 * 加载界面
 */

cc.Class({
    extends: cc.Component,

    properties: {

    },

    // use this for initialization
    onLoad: function () {
        cc.view.setDesignResolutionSize(1136,720, cc.ResolutionPolicy.EXACT_FIT );
        this.node.runAction(cc.sequence(cc.delayTime(0.3),cc.callFunc(function(){
            cc.director.loadScene('LoginScene');
        })))
    },

    // called every frame, uncomment this function to activate update callback
    update: function (dt) {

    },
});
