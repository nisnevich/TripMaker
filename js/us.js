// ==UserScript==
// @name         TripMaker AS assistant
// @namespace    https://search.aviasales.ru/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://search.aviasales.ru/*?*delta=*range=*
// @grant        none
// @require http://code.jquery.com/jquery-1.12.4.min.js
// ==/UserScript==
// example       https://search.aviasales.ru/MOW0803BER1?delta=0&range=1

function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

INTERVAL_CHECK_LOADING = 2000; // in ms
DELTA_TIME_LOADING_XHR_MAX = 10000; // in ms
MIN_DELAY_RELOAD = 15000; // in ms
timestamp_xhr_last_loading = -1;
delta = Number(getUrlParameter("delta"));
range = Number(getUrlParameter("range"));
time_loaded = new Date();

(function() {
    'use strict';
    console.log("TripMaker AS assistant loaded");

    function addXMLRequestCallback(callback){
        var oldSend, i;
        if( XMLHttpRequest.callbacks ) {
            // we've already overridden send() so just add the callback
            XMLHttpRequest.callbacks.push( callback );
        } else {
            // create a callback queue
            XMLHttpRequest.callbacks = [callback];
            // store the native send()
            oldSend = XMLHttpRequest.prototype.send;
            // override the native send()
            XMLHttpRequest.prototype.send = function(){
                // process the callback queue
                // the xhr instance is passed into each callback but seems pretty useless
                // you can't tell what its destination is or call abort() without an error
                // so only really good for logging that a request has happened
                // I could be wrong, I hope so...
                // EDIT: I suppose you could override the onreadystatechange handler though
                for( i = 0; i < XMLHttpRequest.callbacks.length; i++ ) {
                    XMLHttpRequest.callbacks[i]( this );
                }
                // call the native send()
                oldSend.apply(this, arguments);
            };
        }
    }

    addXMLRequestCallback(function (xhr) {
        if (xhr && xhr.url) {
            if (xhr.url.includes("searches_results_united")) {
                timestamp_xhr_last_loading = new Date();
                console.log("TripMaker: Time refreshed.");
            }
        } else {
            console.log("TripMaker: Look, an XHR without URL:");
            console.log(xhr);
        }
    });

    function checkLoadingStatus() {
        if (// if countdown timer is missing
            // $("div.countdown__timer").length === 0
            // if any XHR requests has been sent
            timestamp_xhr_last_loading != -1
            // if time interval since last XHR request has exceeded
            && new Date() - timestamp_xhr_last_loading > DELTA_TIME_LOADING_XHR_MAX
            // if tickets are rendered
            // && ($("div.ticket__container").length > 0
                // or not found
                // || $(".system-message").html().includes("Билеты не найдены"))
            // if status of ticket is rendered ()
            // && $("div.prediction__advice").length > 0
            // to prevent our blocking on server, check that some time passed since page was loaded
            // && new Date() - time_loaded > MIN_DELAY_RELOAD
        ) {
            loadNext();
        } else {
            setTimeout(function(){checkLoadingStatus();}, INTERVAL_CHECK_LOADING);
        }
    }

    function loadNext() {

        if (isNaN(delta) || isNaN(range)) {
            console.error("TripMaker: incorrect input data. delta='" + delta + "', range='" + range + "'");
            return;
        }

        var pathname_params = window.location.pathname.match( /\/([^0-9]{3})([0-9]{2})([0-9]{2})([^0-9]{3})([0-9]{1})/ );

        var orig_city = pathname_params[1];
        var day = Number(pathname_params[2]);
        var month = Number(pathname_params[3]);
        var dest_city = pathname_params[4];
        var count_person = Number(pathname_params[5]);

        var date = new Date();
        if (Math.abs(delta) === range) {
            if (delta < 0) {
                delta = 1; // to increment later
                date.setMonth(month - 1, day + range + 1);
            } else {
                console.log("TripMaker: loading has finished");
                return;
            }
        } else {
            var delta_value = (delta <= 0) ? -1 : 1;
            delta += delta_value;
            date.setMonth(month - 1, day + delta_value);
        }

        var params = "delta=" + delta + "&range=" + range;

        function addLeadZero(n){return n<10? '0'+n:''+n;}
        var path = "/" + orig_city + addLeadZero(date.getDate()) + addLeadZero(date.getMonth() + 1) + dest_city + count_person;
        window.location.href = window.location.origin + path + "?" + params;
    }

    checkLoadingStatus();
})();