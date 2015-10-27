/**
 * Created by Arvin on 2015-10-15.
 */
(function($){
  $.fn.model_grid = function(option){
    var self = this.get(0);
    var t = $(self).find("#data-table");
    var grid = {
      pk:null,
      app_label: null,
      model_name: null,
      heads:[],
      columns: [],
      columnDefs: [],
      checkbox: true,
      operation: true,
      table: null,
      actions: [],
      layer: layer,
      action_form: "#id_action_form",
      row_actions: [
        {action_name: 'ModelDelete', style:'btn-danger', verbose_name: $.i18n.prop('Delete'), row_only: false},
        {action_name: 'ModelEdit', style:'btn-primary', verbose_name:$.i18n.prop('Edit'),row_only: true}
      ],
      default_table_option: {
        "dom": '<"row" <"#toolbar.col-sm-12">>rt<"row" <"col-sm-5" l><"col-sm-4" i><"col-sm-3" p>><"clear">',
        "scrollY": 300,
        "searching": false,
        "ordering": false,
        "select": true
      },
      render_heads: function(){
        var g = self.grid;
        var thead = document.createElement('thead');
        var h_tr = document.createElement("tr");
        for(var i=0; i < g.heads.length; i++){
          var head = g.heads[i];
          if(head.key == "id" && g.checkbox){
            var cbox = '<th style="width:15px"><input type="checkbox" id="checkAll"></th>';
            g.columns.push({
              data: "id",
              fnCreatedCell: function (nTd, sData, oData, iRow, iCol) {
           $(nTd).html("<input type='checkbox' name='checkList' value='" + sData + "'>");
       }
            })
            $(h_tr).append(cbox);
          }else{
            var h_th = document.createElement('th');
            h_th.innerHTML = head.name;
            g.columns.push({'data': head.key});
            $(h_tr).append(h_th);
          }
        };
        if(g.operation){
          var op = '<th style="max-width: 150px">Operation</th>';
          $(h_tr).append(op);
        }
        $(thead).append(h_tr);
        $(t).append(thead);
        $(t).find("#checkAll").click(function () {
            $("input[name='checkList']").prop("checked", this.checked);
        });
      },
      render_row: function(){
        var g = self.grid;
        var targets = g.columns.length;
        console.log("targets"+targets)
        g.columnDefs.push({
            "targets": targets,
            "render": function(a, b, c, d){
              var op = '<a id="{0}" class="button-padding button-margin btn {1}" >{2}</a>';
              var ops = [];
              for(var i=0; i< g.row_actions.length; i++){
                var row_action = g.row_actions[i];
                var action_name = row_action.action_name;
                var action = row_action.action;
                var op_id = "id_{0}_{1}".format(action_name, a.id)
                var op_dom = op.format(op_id, row_action.style, row_action.verbose_name);
                var url = "/model/action/{0}/{1}/{2}/".format(g.app_label, g.model_name, action_name);
                if(action_name == "ModelEdit"){
                  url = "/model/action/{0}/{1}/{2}/".format(g.app_label, g.model_name, a.id);
                }
                if(action.model_action == 'true'){
                  g.render_model_action(t, op_id, url, action);
                }
                if(action.object_action == 'true'){
                  var params = {};
                  params[g.pk] = [a.id];
                  g.render_object_action(t, op_id, url, action, params, action.verbose_name)
                }
                ops.push(op_dom);
              }
              return ops.join("");
            }
        })
        g.columns.push({'data': null});
      },
      get_action: function(action_name){
        var g = self.grid;
        for(var i=0; i< g.actions.length; i++){
          var action = g.actions[i];
          if(action.action_name == action_name){
            return action
          }
        }
        return false;
      },
      row_action_filter: function(){
        var g = self.grid;
        var del = [];
        for(var i=0; i< g.row_actions.length; i++){
          var row_action = g.row_actions[i];
          var action_name = row_action.action_name;
          var action = g.get_action(action_name);
          if(action){
            row_action.action = action;
            if(row_action.row_only){
              g.actions.splice(g.actions.indexOf(action), 1)
            }
          }else{
            del.push(i);
          }
        }
        for(var j in del.reverse()){
          g.row_actions.splice(j, 1);
        }
      },
      get_table_option: function(){
        var g = self.grid;
        var url = "/model/grid/{0}/{1}/".format(g.app_label, g.model_name);
        var option = {
            "ajax": {
                "url": url,
                "dataType": 'json'
            },
            "columns": g.columns,
            "columnDefs": g.columnDefs
        }
        return $.extend(g.default_table_option, option);
      },
      init_table: function(reload){
        var g = self.grid;
        if(reload){
          g.render_heads();
          g.render_row();
          g.table = $(t).dataTable(g.get_table_option());
        }
      },
      action_ajax: function(ajaxAttrs, successCallback, errorCallback){
        $.ajax({
          url: ajaxAttrs.url,
          type: ajaxAttrs.type,
          traditional: ajaxAttrs.traditional?ajaxAttrs.traditional:false,
          dataType: ajaxAttrs.dataType,
          async: ajaxAttrs.async?ajaxAttrs.async:true,
          data: ajaxAttrs.data,
          success: successCallback,
          error: errorCallback //XMLHttpRequest, textStatus, errorThrow
        });
      },
      render_model_action: function(container, action_id, url, action){
        var g = self.grid;
        $(container).off('click', '#{0}'.format(action_id)).on('click', '#{0}'.format(action_id), function() {
          var successCallback = function(html){
            $("#edit-content").append(html).show();
            $("#edit-content").on('click', '.form-actions a.btn', function(){
              var form = $("#edit-content").find("#id_model_form");
              var form_callback = function(callback){
                var info = $("#edit-content").find('#id_info');
                var ret= callback.ret;
                var message = callback.message;
                if(ret == 'success'){
                   $(info).addClass('alert-success');
                   $(info).html(message);
                   g.table.fnReloadAjax();
                   $("#edit-content").empty();
                   $("#content").show();
                }
                if(ret == 'failed'){
                  for(var key in message){
                    $(info).addClass('alert-danger');
                    $("input[name="+key+"]").focus();
                    $(info).html(message[key][0]['message']);
                  }
                }
              }
              var attrs = {url:url, type:"POST", dataType:"json", data:$(form).serialize()};
              g.action_ajax(attrs, form_callback);
            });
            $("#content").hide();
          };
          var attrs = {url:url, type:'Get', dataType:'html'};
          g.action_ajax(attrs, successCallback)
        });
      },
      get_formData: function(formArray, data){
        var formData = {};
        for(var i=0; i<formArray.length; i++){
          var d = formArray[i];
          formData[d.name] = d.value;
        }
        return $.extend(formData, data)
      },
      render_object_action: function(container, action_id, url, action, params, title){
        var g = self.grid;
        var layer = g.layer;
        var pk = g.pk;
        $(container).off('click', '#{0}'.format(action_id)).on('click', '#{0}'.format(action_id), function(){
          if(params == undefined) {
            var checkList = $(g.table).find("input[name='checkList']:checked");
            var data = {};
            data[pk] = [];
            $.each(checkList, function () {
              data[pk].push($(this).val());
            });
          }else{
            var data = params;
          }
          if (data[pk].length == 0) {
            layer.msg($.i18n.prop("Please select the object(s)"), {icon: 2});
          } else {
            var attrs = {url:url, data:data, type:'GET', dataType:'html', traditional:true};
            var successCallback = function(html){
              layer.open({
                  type: 1,
                  area: ['auto', 'auto'],
                  title: title?title:$.i18n.prop("Number of selected: {0}", data[pk].length),
                  shadeClose: true,
                  content: html,
                  btn: [$.i18n.prop('Sure'), $.i18n.prop('Cancel')],
                  yes: function(index, layero){
                    var formdata = g.get_formData($(g.action_form).serializeArray(), data);
                    var formcallback = function(callback){
                      var ret = callback.ret;
                      var message = callback.message;
                      if(ret == "failed"){
                        layer.msg(message, {icon: 2});
                      }
                      if(ret == "success"){
                        g.table.fnReloadAjax();
                        layer.close(index);
                        layer.msg(message, {icon: 1});
                      }
                    };
                    var form_attrs = {url:url, data:formdata, type:'POST', dataType:'json', traditional:true};
                    g.action_ajax(form_attrs, formcallback);
                  },
                  cancel: function(index){}
              });
            };
            g.action_ajax(attrs, successCallback);
          };
        });
      },
      render_action: function(action){
        var g = self.grid;
        var url = "/model/action/{0}/{1}/{2}/".format(g.app_label, g.model_name, action['action_name']);
        if (action['model_action'] == 'true') {
          var action_id = "id_model_{0}".format(action['action_name']);
          var action_dom = '<li id="{0}" ><a href="javascript:void(0)">{1}</a></li>'.format(action_id, action['verbose_name']);
          $("#model_actions .dropdown-menu").append(action_dom);
          g.render_model_action(self, action_id, url, action);
        }else if(action['object_action'] == 'true'){
          var action_id = "id_obj_{0}".format(action['action_name']);
          var action_dom = '<div id="{0}" class="btn-group"><a href="javascript:void(0)" class="btn">{1}</a><div>'.format(action_id, action['verbose_name']);
          $("#data-table_wrapper #toolbar").append(action_dom);
          g.render_object_action(self, action_id, url, action);
        }
      },
      init_toolbar: function(){
        var g = self.grid;
        var actions= g.actions;
        for(var i in actions) {
          g.render_action(actions[i]);
        }
      },
      render_row_event: function(){
        var g = self.grid;
        if(!g.table){
          g.init_table(true);
        }
      },
      init_grid: function(){
        var g = self.grid;
        g.row_action_filter()
        g.init_table(true);
        g.init_toolbar();
        g.render_row_event();
      }
    };
    $.extend(grid, option);
    self.grid = grid;
    if(!self.grid.pk){
      self.grid.pk = 'id';
    }
    grid.init_grid();
  }
})(jQuery)

