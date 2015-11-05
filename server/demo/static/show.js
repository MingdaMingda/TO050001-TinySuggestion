// Copyright 2009 FriendFeed
//
// Licensed under the Apache License, Version 2.0 (the "License"); you may
// not use this file except in compliance with the License. You may obtain
// a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
// WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
// License for the specific language governing permissions and limitations
// under the License.

function show_result() {
    show_sugg_result();
}

function show_sugg_result() {
    var a = document.getElementById("q");
    var q = a.value;
    if (q == "") {
        console.log("blank query");
        return;
    }
    console.log(q);

    var url="r/sugg/?q=" + encodeURI(q);

    var xmlHttp=new XMLHttpRequest();
    xmlHttp.open("GET", url, false);
    xmlHttp.send(null);
    var xmlDoc=xmlHttp.responseText;

    var a = document.getElementById("sugg_result");
    a.innerHTML = xmlDoc;
}

