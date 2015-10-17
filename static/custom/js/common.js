$(function ()
{
   var execute_status, all_tree, reg_user, db_status;
   $.ajax({
           url:"/echarts/",
          async:false,
          success:function(data){
          var jsondata= JSON.parse(data);
          execute_status = jsondata.dbaction_status;
          all_tree = jsondata.all_tree;
          reg_user = jsondata.reg_user;
          db_status = jsondata.db_status;
       }
   
    });
    // 路径配置
    require.config({
        paths: {
//            echarts: 'http://echarts.baidu.com/build/dist'
            echarts: '/static/custom/js/build/dist'
        }
    });
  // 使用
    require(
        [
            'echarts',
            'echarts/chart/bar', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/line', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/pie', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/funnel', // 使用柱状图就加载bar模块，按需加载
            'echarts/chart/tree', // 使用柱状图就加载bar模块，按需加载
        ],
        function (ec) {
            // 基于准备好的dom，初始化echarts图表
           var my_execute_status = ec.init(document.getElementById('execute_status')); 
           var my_all_tree = ec.init(document.getElementById('all_tree')); 
           var my_reg_user = ec.init(document.getElementById('reg_user')); 
           var my_db_status = ec.init(document.getElementById('db_status')); 
           option1 = {
            title : {
                text: 'DB变更申请状态',
                subtext: '状态',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data:['已通过','已取消','待审核']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true, 
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 335
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'变更状态统计',
                    type:'pie',
                    radius : '55%',
                    center: ['50%', '60%'],
                    data:execute_status
                }
            ]
        };

        option2 = {
            title : {
                text: '项目树形图表'
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            series : [
                {
                    name:'树图',
                    type:'tree',
                    orient: 'horizontal',  // vertical horizontal
                    rootLocation: {x: 100,y: 230}, // 根节点位置  {x: 100, y: 'center'}
                    nodePadding: 8,
                    layerPadding: 200,
                    hoverable: false,
                    roam: true,
                    symbolSize: 6,
                    itemStyle: {
                        normal: {
                            color: '#4883b4',
                            label: {
                                show: true,
                                position: 'right',
                                formatter: "{b}",
                                textStyle: {
                                    color: '#000',
                                    fontSize: 5
                                }
                            },
                            lineStyle: {
                                color: '#ccc',
                                type: 'dashed' // 'curve'|'broken'|'solid'|'dotted'|'dashed'
        
                            }
                        },
                        emphasis: {
                            color: '#4883b4',
                            label: {
                                show: true
                            },
                            borderWidth: 0
                        }
                    },
                    
                    data: all_tree
                    
                }
            ]
        };


        option3 = {
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data:['管理员','普通用户']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true, 
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'center',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'注册用户',
                    type:'pie',
                    radius : ['50%', '70%'],
                    itemStyle : {
                        normal : {
                            label : {
                                show : false
                            },
                            labelLine : {
                                show : false
                            }
                        },
                        emphasis : {
                            label : {
                                show : true,
                                position : 'center',
                                textStyle : {
                                    fontSize : '30',
                                    fontWeight : 'bold'
                                }
                            }
                        }
                    },
                    data: reg_user
                }
            ]
        };

        option4 = {
            title : {
                text: '数据库连接状态',
                subtext: '',
                x:'center'
            },
            tooltip : {
                trigger: 'item',
                formatter: "{a} <br/>{b} : {c} ({d}%)"
            },
            legend: {
                orient : 'vertical',
                x : 'left',
                data:['正在连接','连接成功','连接失败']
            },
            toolbox: {
                show : true,
                feature : {
                    mark : {show: true},
                    dataView : {show: true, readOnly: false},
                    magicType : {
                        show: true, 
                        type: ['pie', 'funnel'],
                        option: {
                            funnel: {
                                x: '25%',
                                width: '50%',
                                funnelAlign: 'left',
                                max: 1548
                            }
                        }
                    },
                    restore : {show: true},
                    saveAsImage : {show: true}
                }
            },
            calculable : true,
            series : [
                {
                    name:'连接状态',
                    type:'pie',
                    radius : '55%',
                    center: ['50%', '60%'],
                    data: db_status
                    
                }
            ]
        };
                    
            // 为echarts对象加载数据 
            my_execute_status.setOption(option1); 
            my_all_tree.setOption(option2); 
            my_reg_user.setOption(option3); 
            my_db_status.setOption(option4); 
        }
    );
});



