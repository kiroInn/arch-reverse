/**
 * Created by bot.su on 2017/5/7.
 */
/**
 * Created by bot.su on 2017/5/7.
 * 登录界面
 */

cc.Class({
    extends: cc.Component,

    properties: {
        _labelCoin: {
            default: null,
            type: cc.Label
        },
    },

    // use this for initialization
    onLoad: function () {
        cc.view.setDesignResolutionSize(1136,720, cc.ResolutionPolicy.EXACT_FIT );


        var node = this.node.getChildByName("node_header");
        this._labelCoin = node.getChildByName("label_coin").getComponent(cc.Label);
        this._labelRankName = node.getChildByName("label_rankName").getComponent(cc.Label);
        this._labelRankScore = node.getChildByName("label_rankScore").getComponent(cc.Label);


        this._labelCoin.string = "金币：100001234567";


        //测试通知
        this.node.runAction(cc.sequence(cc.delayTime(1),cc.callFunc(function(){
            this.notify();
        }.bind(this))));
    },


    //来自服务器的通知
    notify:function(){
        var node = this.node.getChildByName("node_notify");
        var sprite = node.getChildByName("sprite_notifyBg").getComponent(cc.Sprite);
        var label = node.getChildByName("label_notify").getComponent(cc.Label);
        node.active=true;
        label.string = "大家好我是最叼的那个人";
        var dis = label.node.width+sprite.node.width;
        label.node.x = dis/2;

        sprite.node.runAction(cc.sequence(cc.scaleTo(1,1,1),
            cc.delayTime(dis/100),
            cc.scaleTo(1,0,1),
            cc.callFunc(function(){
                node.active = false;
            })));
        label.node.runAction(cc.moveBy(dis/100,cc.p(-dis,0)));
    },

    // called every frame, uncomment this function to activate update callback
    update: function (dt) {

    },
});
