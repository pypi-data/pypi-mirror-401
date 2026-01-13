let fontDict = {
    '00智能体': {'icon': 'fas fa-robot', 'color': '#3498db'},
    '01仪表盘': {'icon': 'fas fa-tachometer-alt', 'color': '#2ecc71'},
    '05连接池': {'icon': 'fas fa-network-wired', 'color': '#e74c3c'},
    '07项目': {'icon': 'fas fa-project-diagram', 'color': '#9b59b6'},
    '其它日志': {'icon': 'fas fa-clipboard-list', 'color': '#95a5a6'},
    '图形管理': {'icon': 'fas fa-chart-line', 'color': '#1abc9c'},
    '访问记录': {'icon': 'fas fa-user-clock', 'color': '#f39c12'},
    '01任务计划': {'icon': 'fas fa-calendar-alt', 'color': '#34495e'},
    '02上传设定': {'icon': 'fas fa-upload', 'color': '#16a085'},
    '03下载设定': {'icon': 'fas fa-download', 'color': '#16a085'},
    '03质量记录': {'icon': 'fas fa-clipboard-check', 'color': '#e67e22'},
    '源表关系': {'icon': 'fas fa-sitemap', 'color': '#8e44ad'},
    '血缘关系': {'icon': 'fas fa-code-branch', 'color': '#d35400'},
    '表结构': {'icon': 'fas fa-table', 'color': '#27ae60'},
    '质量类型': {'icon': 'fas fa-tags', 'color': '#c0392b'},
    '组': {'icon': 'fas fa-users', 'color': '#2980b9'},
    '用户': {'icon': 'fas fa-user', 'color': '#2980b9'},
    '01报表资产': {'icon': 'fas fa-chart-pie', 'color': '#e74c3c'},
    '02数据质量': {'icon': 'fas fa-check-circle', 'color': '#2ecc71'},
    '执行记录': {'icon': 'fas fa-tasks', 'color': '#f1c40f'},
    '访问设定': {'icon': 'fas fa-key', 'color': '#9b59b6'},
    '应用服务': {'icon': 'fas fa-server', 'color': '#7f8c8d'},
    '上传下载': {'icon': 'fas fa-exchange-alt', 'color': '#3498db'},

    'SmartChart': {'icon': 'fas fa-chart-line', 'color': '#3498db'},
    '大数据管道': {'icon': 'fas fa-project-diagram', 'color': '#e74c3c'},
    '指标管理': {'icon': 'fas fa-sliders-h', 'color': '#9b59b6'},
    '数据治理': {'icon': 'fas fa-database', 'color': '#2ecc71'},
    '认证和授权': {'icon': 'fas fa-user-shield', 'color': '#f39c12'},
    '预留接口': {'icon': 'fas fa-plug', 'color': '#95a5a6'},
    'DX基础模板': {'icon': 'fas fa-file-code', 'color': '#3498db'},
    'DX模板': {'icon': 'fas fa-file-alt', 'color': '#2ecc71'},
    '传输记录': {'icon': 'fas fa-exchange-alt', 'color': '#e74c3c'},
    '租户管理': {'icon': 'fas fa-users-cog', 'color': '#9b59b6'},
    '指标类别': {'icon': 'fas fa-tags', 'color': '#1abc9c'},
    '指标项目': {'icon': 'fas fa-chart-bar', 'color': '#f39c12'},
    '00数据资产': {'icon': 'fas fa-database', 'color': '#3498db'},
    '任务监控': {'icon': 'fas fa-tasks', 'color': '#e74c3c'},
    '固定值API': {'icon': 'fas fa-code', 'color': '#9b59b6'}
}

function getIcon(name, icon){
    if(!name){return;}
    if(fontDict.hasOwnProperty(name)){return fontDict[name].icon}
    return icon||'far fa-circle';
}
function getColor(name){
    if(fontDict.hasOwnProperty(name)){return fontDict[name].color}
    return '';
}