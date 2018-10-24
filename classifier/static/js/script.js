var selectedElement = null;

var elementData = null;

$(document).ready(function() {
    $(".editor").hide();

    $.ajax({
            method: "GET",
            url: "/api/elements",
            success: function(data) {
                console.log("Init data :");
                console.log(data);
                initialize(data)
            },
            error: function() {
                alert("O-o-ops, what the problem?");
            }
        });

    // $(".menu-search").change(function(){
    //     $(".element p").each(function(key, value){
    //         console.log(value.innerText);
    //         if(value.innerText.indexOf >= 0){
    //             value
    //         }
    //     });
    // });
});

function addElement(element) {
    text = `
                    <div id="${element["id"]}" class="element">
                        <a href=""></a>
                        <p>${element["elementName"]}</p>
                        <div class="childElements" style="display:none">
                    </div>
                `;
    parentElementId = element["parentElementId"];
    if (parentElementId === -1) {
        $("#-1").append(text);
    } else {
        rule = `#${parentElementId}`;
        $(rule).children(".childElements").append(text);
    }
    return element["id"];
}

function constructObject(elementName = "Name", id = -1,
                         isEnd = false, isIndexed = true,
                         isRoot = true, parentElementId = -1) {
/*{
  "elementName": "Kangaroo",
  "id": 0,
  "isEnd": 0,
  "isIndexed": 1,
  "isRoot": 1,
  "parentElementId": -1
}*/

    obj = {
        "elementName" : elementName,
        "id" : id,
        "isEnd" : isEnd,
        "isIndexed" : isIndexed,
        "isRoot" : isRoot,
        "parentElementId" : parentElementId,
    };

    return obj;
}

function listClick(event) {
    event.preventDefault();
    var $answer = $(this).first().parent().children().next('.childElements');
    console.log($answer);
    if ($answer.is(':hidden')) {
        $answer.slideDown();
        //$answer.fadeIn();
        $(this).addClass('close');
    } else {
        $answer.slideUp();
        //$answer.fadeOut();
        $(this).removeClass('close');
    }
}

function elementClick() {
    if (selectedElement == null) {
        selectElement($(this));
    } else {
        if ($(this).is(selectedElement)) {
            deselectElement();
            return;
        } else {
            deselectElement();
            selectElement($(this));
        }
    }

    $.ajax({
        method: "GET",
        url: "/api/element/" + $(this).parent().attr("id"),
        success: function (data) {
            console.log(data);
            fillEditor(data);
            elementData = data;
        },
        error: function () {
            alert("Check console there is nothing");
        }
    });
}

function addParentListGroup(item) {
    if(item['isEnd'])
        return false;
    $("#parentElementId")
        .append($("<option></option>")
            .attr("value", item['id'])
            .text(item['elementName'])
    );

    return true;
}

function initialize(data) {
     //Load data
    data.forEach(function(item, i, arr) {
        addElement(item);
        addParentListGroup(item);
    });

    $('.childElements').hide();

	$('.menu-list-elements p').click(elementClick);
        /*.dblclick(function() {
            var $answer = $(this).next('.childElements');
            console.log($answer);
            if ($answer.is(':hidden')) {
                $answer.slideDown();
                //$answer.fadeIn();
                $(this).addClass('close');
            } else {
                $answer.slideUp();
                //$answer.fadeOut();
                $(this).removeClass('close');
            }
        });*/

	$(".menu-list-elements a").click(listClick);

	$('#menu-add-new-element').click(function(){
        let parentElementId = -1;
	    if(selectedElement != null){
            parentElementId = parseInt(selectedElement.parent().attr("id"));
        }
        let CreateElement = constructObject();
	    CreateElement.parentElementId = parentElementId;
	    $.ajax({
            method: "POST",
            url: "/api/element",
            contentType : 'application/json',
            data: JSON.stringify(CreateElement),
            success: function(data) {
                console.log(data);

                fillEditor(data);

                new_id = addElement(data);
                rule = "#" + new_id;
                $(rule).children().next("p").click(elementClick);
                $(rule).children().closest("a").click(listClick);

                $parent = $(rule).parent();

                debugCounter1 = 0;

                while($parent.attr('id') !== "-1") {
                    if(debugCounter1++ > 50) {
                        console.log("debugCounter1 overflow!!!");
                        break;
                    }
                    if($parent.attr('id') !== undefined && $parent.children().next('.childElements').is(":hidden")){
                        $parent.children().next('.childElements').fadeIn();
                        $parent.children().closest('a').addClass('close');
                    }
                    $parent = $parent.parent();
                }

	            selectElement($(rule).children().next("p"));
                enableEditor();
            },
            error: function(textStatus) {
                alert("Check console");
                console.log(textStatus.responseJSON);
            }
        });
    });

	$("#editor-save").click(function(){
	    elementDetails = {
	        "elementName" : $("#elementName").val(),
            "isRoot" : $("#isRoot").prop("checked"),
            "isIndexed" : $("#isIndexed").prop("checked"),
            "isEnd" : $("#isEnd").prop("checked"),
            "id" : parseInt($("#editor-id").val()),
            "parentElementId" : parseInt($("#parentElementId").val()),
        };

	    $.ajax({
            method: "PUT",
            url: "/api/element/" + $("#editor-id").val(),
            contentType : 'application/json',
            data: JSON.stringify(elementDetails),
            success: function(data) {
                console.log(data);
                id = $("#editor-id").val();
                disableEditor();
                deselectElement();

                if(elementData['parentElementId'] !== data['parentElementId']){
                    rule = "#" + data['id'];
                    rule2 = "#" + data['parentElementId'];
                    if(data['parentElementId'] !== -1)
                        $(rule).appendTo($(rule2).children().next('.childElements'));
                    else
                        $(rule).appendTo("#0");
                }

                if(elementData['elementName'] !== data['elementName']) {
                    rule = "#" + data['id'];
                    $(rule).children().closest('p').text(data['elementName']);

                    $(`option[value='${data['id']}']`).text(data['elementName'])
                }
            },
            error: function(textStatus) {
                alert("Check console");
                console.log(textStatus.responseJSON);
            }
        });
    });

	$("#editor-delete").click(function(){

	    $.ajax({
            method: "DELETE",
            url: "/api/element/" + $("#editor-id").val(),
            success: function(data) {
                console.log(data);
                id = $("#editor-id").val();
                $("#" + id).remove();
                deselectElement();
            },
            error: function(textStatus) {
                alert("Check console");
                console.log(textStatus.responseJSON);
            }
        });
    });

	$("#editor-cancel").click(function(){
	    deselectElement();
    });
}

function enableEditor() {
    $('.editor').show();
}

function disableEditor() {
    $(".editor").hide();
}

function selectElement(element) {
    if(selectedElement != null) {
        deselectElement();
    }
    selectedElement = element;
    selectedElement.css("background-color", "chocolate");
    //enableEditor(element);
}

function deselectElement() {
    selectedElement.removeAttr("style");
    selectedElement = null;
    disableEditor();
}

function fillEditor(data) {
    /*{
  "elementName": "Kangaroo",
  "id": 0,
  "isEnd": 0,
  "isIndexed": 1,
  "isRoot": 1,
  "parentElementId": -1
}*/
    $("#elementName").val(data["elementName"]);
    $("#isRoot").prop("checked", data['isRoot']);
    $("#isIndexed").prop("checked", data['isIndexed']);
    $("#isEnd").prop("checked", data['isEnd']);
    $("#editor-id").val(data["id"]);
    $("#parentElementId").val(data['parentElementId']);

    enableEditor();
}