function readFile(input) {
    if (input.files && input.files[0]) {
      var reader = new FileReader();
  
      reader.onload = function(e) {
        var htmlPreview =
          '<img width="200" src="' + e.target.result + '" />' +
          '<p>' + input.files[0].name + '</p>';
        var wrapperZone = $(input).parent();
        var previewZone = $(input).parent().parent().find('.preview-zone');
        var boxZone = $(input).parent().parent().find('.preview-zone').find('.box').find('.box-body');
  
        wrapperZone.removeClass('dragover');
        previewZone.removeClass('hidden');
        boxZone.empty();
        boxZone.append(htmlPreview);
      };
  
      reader.readAsDataURL(input.files[0]);
    }
  }
  
  function reset(e) {
    e.wrap('<form>').closest('form').get(0).reset();
    e.unwrap();
  }
  
  $(".dropzone").change(function() {
    readFile(this);
  });
  
  $('.dropzone-wrapper').on('dragover', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).addClass('dragover');
  });
  
  $('.dropzone-wrapper').on('dragleave', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $(this).removeClass('dragover');
  });
  
  $('.remove-preview').on('click', function() {
    var boxZone = $(this).parents('.preview-zone').find('.box-body');
    var previewZone = $(this).parents('.preview-zone');
    var dropzone = $(this).parents('.form-group').find('.dropzone');
    boxZone.empty();
    previewZone.addClass('hidden');
    reset(dropzone);
  });
  

//   카테고리 js
$(document).ready(function(){

    //DropDown input - select
    $('.t-dropdown-input').on('click', function() {
        $(this).parent().next().slideDown('fast');
    });
    
    $('.t-select-btn').on('click', function() {
       $('.t-dropdown-list').slideUp('fast');
    
        if(!$(this).prev().attr('disabled')){
        $(this).prev().trigger('click');
        }
    });
    
    $('.t-dropdown-input').width($('.t-dropdown-select').width() - $('.t-select-btn').width() - 13);
    
    $('.t-dropdown-list').width($('.t-dropdown-select').width());
    
    $('.t-dropdown-input').val('');
    
    $('li.t-dropdown-item').on('click', function() {
      var text = $(this).html();
      $(this).parent().prev().find('.t-dropdown-input').val(text);
      $('.t-dropdown-list').slideUp('fast');
    });
    
    $(document).on('click', function(event) {
      if ($(event.target).closest(".t-dropdown-input, .t-select-btn").length)
        return;
      $('.t-dropdown-list').slideUp('fast');
      event.stopPropagation();
    });
    // END //
    
    });


    // 포스트박스 여닫기
    function openClose() {
        if ($("#post-box").css("display") == "none") {
            $("#post-box").show();
            $("#btn-post-box").text("카테고리 추가");
        }
        else {
            $("#post-box").hide();
        }

    //     if ($("#post-box").css("display") == "block") {
    //         $("#post-box").hide();
    //         $("#btn-post-box").text("카테고리 추가");
    //     } 
    //     else {
    //         $("#post-box").show();
    //         $("#btn-post-box").text("카테고리 저장 닫기");
    //     }
    }