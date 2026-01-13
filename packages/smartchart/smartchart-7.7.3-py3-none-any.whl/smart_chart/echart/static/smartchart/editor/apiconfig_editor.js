$('#submit').click(function () {
    let e = editor1.getValue();
    $.ajax({
        type: "POST",
        url: "/echart/save_apiconfig/",
        data: {option: e},
        success: function (data) {
            $('#printlog').html(data['msg']);
        }
    });
});
editor1.getSession().on('change', function (e) {
    $("#printlog").html('');
});
$('#id_peizhi').html('<li>API样列</li><li>首页配置</li><li>租户配置</li>');
$('#id_peizhi li').click(function () {
    let zj = $(this).text();
    let c;
    if (zj === 'API样列') {
        c = `{"token": "smartchartxxx","limit": 60,"log":1,"cors": 1}`;
    }else if(zj === '租户配置'){
        c = `"tid": {"TNT": {"id":1,"title": "xx"}}`;
    }else if(zj === '首页配置'){
        c = `
 "SMC": {
    "logo": "/.../xx.png",
    "title": "数据中台",
    "logoWidth": "130px",
    "gpt":"smtgpt",
    "home":"/echart/?type=2",
    "theme":"/static/smartui/theme/light.css"
  }，
 "_SMC": {
    "admin": {"title": "个性化","logo": "//.../xx.png"}
  }
`;
    }
    if (c) {editor1.insert(c);}
});