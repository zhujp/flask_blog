/**
 * 定义layui 基础模块
 * 
 * @param  {[type]} exports){               var layer [description]
 * @return {[type]}            [description]
 */
layui.define(['layer', 'form', 'element', 'upload', 'laydate','table'], function(exports){
    var $ = layui.jquery
        ,element = layui.element
        ,laydate = layui.laydate
        ,form = layui.form
        ,table = layui.table
        ,upload = layui.upload
        ,layer = layui.layer;

    $.ajaxSetup({
        headers: {
            // 'X-CSRF-TOKEN': $('input[name="_csrf-backend"]').val()
            'X-CSRF-TOKEN': $('meta[name="csrf_token"]').attr('content')
        }
    });

    function ajaxRequest(url,data,method,redirect)
    {
        $.ajax({
            url:url,
            data:data,
            type:method,
            dataType:"json",
            success:function(result){
              if (result.code == 1) {
                layer.msg(result.msg);
                if (redirect == 1) {
                    setInterval(function(){
                        window.location.href=result.url;
                    },result.wait*1000);
                }
                return false;
              }
              layer.msg(result.msg);
            }
        });
    }
    table.on('tool(backend-table)', function(obj){
        var data = obj.data;
        var pkey = 'id';
        if(typeof($(this).attr("data-pkey"))!="undefined") {
            pkey = $(this).attr("data-pkey");
        }
        var id = $(this).attr('data-id');
        if (typeof($(this).attr("data-id"))=="undefined") {
            id = data.id;
        }
        var url = $(this).attr('data-url')+'?'+pkey+'='+id;
        if(obj.event === 'detail'){
            window.location.href = url;
        } else if(obj.event === 'del'){
            layer.confirm('确定删除数据吗', function(index){
                ajaxRequest(url,'','GET',0);
                obj.del();
                layer.close(index);
            });
        } else if(obj.event === 'edit'){
            window.location.href = url;
        }else{
            window.location.href = url;
        }
    });

    //监听表单提交
    form.on('submit(form-save)', function(data){
        var method = data.field._method;
        if (method == '' || method == null) {
            method = 'POST';
        }
        if (typeof simplemde != "undefined") {
            data.field.body = simplemde.value();
            $('#md').val(simplemde.value());
        } 
        //修改提交格式
        var new_data = $(data.form).serialize(); //此处新增表单数据提交方式
        ajaxRequest(data.form.action,new_data,method,1);
        return false;
    });


    element.on('tab(tab-lists)', function(obj){
       var url = $(this).attr('data-url');
       if (typeof(url) == 'undefined' || url == '') {
        return false;
       }
       location.href = url;
    });
    

    var $ = layui.$, active = {
      reload: function(){
        var demoReload = $('#table-reload');
        //执行重载
        table.reload('test-table-reload', {
          page: {
            curr: 1 //重新从第 1 页开始
          }
          ,where: {
            key: {
              id: demoReload.val()
            }
          }
        });
      },
      create:function(){
        window.location.href=$(this).attr('data-url');
      }
    };
    
    $('.table-reload-btn .layui-btn').on('click', function(){
      var type = $(this).data('type');
      active[type] ? active[type].call(this) : '';
    });
    
});    