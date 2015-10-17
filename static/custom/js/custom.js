function delete_modal_form(url) {
    if ( ! confirm('确认删除?')) {
       return false; 
    }
    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {
             window.location = window.location;
             window.location.reload(); 

        },
    });
}

function dbaction_ajax_func(url){
        $.ajax({
            type: 'GET',
            url: url,
            success: function (data) {
                 window.location = window.location;
                 window.location.reload(); 

            },
        });
}


$(".form_datetime").datetimepicker({format: 'yyyy-mm-dd hh:ii'});

$.cxSelect.defaults.url = '/dbselect_ajax/';


$('#city_china_val').cxSelect({
  selects: ['project', 'version', 'product', 'dbname'],
  nodata: 'none'
});



function get_db_tables(event){
    var dbname_value = $('#dbname').val();
    if(dbname_value == 0 || dbname_value == ''||dbname_value ==null){
        if (event.type == 'click'){
            alert('请先选择数据库');
        }
        return;
    }
    var sql = $('#sql').val();
    var vertical = $('#vertical').val();
    var url = "/db_tables_ajax/?vertical="+vertical+"&dbstr="+dbname_value;
    if (event.type == 'click'){
        url = "/db_tables_ajax/?vertical="+vertical+"&dbstr="+dbname_value+"&sql="+sql;
    }
    var tables_string;
    if (event.type == 'click'){
        $("#dbselect_status").slideToggle("slow");
        $('#stderr').css('display', 'none');
        $('#stdout').css('display', 'none');
    }
    $.ajax({
        type: 'GET',
        url: url,
        success: function (data) {
            var jsondata= JSON.parse(data);
            var act = jsondata.act;
            var res = jsondata.res;
            $('#stdout').css('display', 'none');
            $('#stderr').css('display', 'none');
            if (act == 'show'){
                var tables_str = new Array();
                var db_html='';
                tables_str = res.split(";");
                for (i=0;i<tables_str.length;i++){
                    if (tables_str[i] == '' || tables_str[i]==null){
                        continue;
                    };
                    temp_html = '<div class="tree-item" style="display: block;"><i class="icon-remove"></i><div class="tree-item-name">'+tables_str[i]+'</div></div>';
                    db_html = db_html+temp_html;
                }
                $('#tree_content_html').html(db_html);
                $('#tree_folder_name').text(dbname_value);
            }
            else if (act == 'stdout'){
                $('#stdout').html(res);
                $('#stdout').css('display', 'block');
            }
            else if (act == 'stderr'){
                $('#stderr').text(res);
                $('#stderr').css('display', 'block');
            }
        if (event.type == 'click'){
            $("#dbselect_status").slideToggle("slow");
        }
        },
    });
}



function appaction_handler(event) {
    var form = $('.appaction');
    $("#icon-spinner").slideToggle("slow");
    $('#stderr').css('display', 'none');
    $('#stdout').css('display', 'none');
    $.post(form.attr('action'), form.serialize(), ajax_handler(form));
}

function ajax_handler(form) {
    return function (data, status, response) {
        var contentType = response.getResponseHeader('Content-Type');
        if (contentType.match(/json/)) {
            if (data.act == 'stdout') {
                $('#stdout').html(data.res);
                $('#stderr').css('display', 'none');
                $('#stdout').css('display', 'block');

            }
            else if (data.act == 'stderr'){
                $('#stderr').html(data.res);
                $('#stdout').css('display', 'none');
                $('#stderr').css('display', 'block');
            }
        }
        $("#icon-spinner").slideToggle("slow");
    }
}

