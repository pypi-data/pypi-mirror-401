var contrastColor = '#eee';
var axisCommon = function() {
    return {
        axisLine: {
            lineStyle: {
                color: contrastColor
            }
        },
        axisTick: {
            lineStyle: {
                color: contrastColor
            }
        },
        axisLabel: {
            textStyle: {
                color: contrastColor
            }
        },
        splitLine: {
            lineStyle: {
                type: 'dashed',
                color: '#aaa'
            }
        },
        splitArea: {
            areaStyle: {
                color: contrastColor
            }
        }
    };
};

var colorPalette = [
    '#00305a',
    '#004b8d',
    '#0074d9',
    '#4192d9',
    '#7abaf2',
    '#99cce6',
    '#d6ebf5',
    '#eeeeee'
];
var theme = {
    color: colorPalette,
    backgroundColor: '#333',
    tooltip: {
        axisPointer: {
            lineStyle: {
                color: contrastColor
            },
            crossStyle: {
                color: contrastColor
            }
        }
    },
    legend: {
        textStyle: {
            color: contrastColor
        }
    },
    title: {
        textStyle: {
            color: contrastColor
        }
    },
    toolbox: {
        iconStyle: {
            normal: {
                borderColor: contrastColor
            }
        }
    },

    // Area scaling controller
    dataZoom: {
        dataBackgroundColor: '#eee', // Data background color
        fillerColor: 'rgba(200,200,200,0.2)', // Fill the color
        handleColor: '#00305a' // Handle color
    },

    timeline: {
        itemStyle: {
            color: colorPalette[1]
        },
        lineStyle: {
            color: contrastColor
        },
        controlStyle: {
            color: contrastColor,
            borderColor: contrastColor
        },
        label: {
            color: contrastColor
        }
    },

    timeAxis: axisCommon(),
    logAxis: axisCommon(),
    valueAxis: axisCommon(),
    categoryAxis: axisCommon(),

    line: {
        symbol: 'circle'
    },
    graph: {
        color: colorPalette
    },

    gauge: {
        axisLine: {
            lineStyle: {
                color: [
                    [0.2, '#004b8d'],
                    [0.8, '#00305a'],
                    [1, '#7abaf2']
                ],
                width: 8
            }
        }
    }
};

theme.categoryAxis.splitLine.show = false;
echarts.registerTheme('dark-blue', theme);