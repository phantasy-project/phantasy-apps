var Ui = {

    initializeView: function () {
        var svg = document.querySelector('svg');
        var w = svg.width.baseVal.value;
        var h = svg.height.baseVal.value;
        CTRL.get_content_size(w, h);
    },

    findDevices: function () {
        var descs = Array.prototype.slice.call(document.querySelectorAll("desc"));
        descs.forEach(function (desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if (result) {
                var devname = result[1],
                    parent = desc.parentNode;
                console.log("Found device: " + devname +
                            " (" + parent.getAttribute("id") + ")");
                CTRL.registerDevice(devname);
                //parent.classList.add('tooltip');
                if (!parent.onclick)
                    parent.onclick = function (evt) {
                        CTRL.select(devname);
                };
                if (!parent.ondblclick)
                    parent.ondblclick = function (evt) {
                        CTRL.dblSelect(devname);
                };
                if (!parent.onmouseover)
                    parent.onmouseover = function (evt) {
                        CTRL.mouseOver(devname);
                };

                // check
                var elems = Ui.getElementsByDeviceName(devname);
                if (elems.length > 1) {
                    console.log(devname + " has more than one elements.");
                };
            }
        });
        CTRL.loadDeviceDone();
    },

    // find anchors for annotations
    findAnnotes: function() {
        var annotes = Array.prototype.slice.call(document.querySelectorAll("desc"));
        annotes.forEach(function (annote) {
            var result = /annote=(.*),(.*)/.exec(annote.textContent);
            if (result) {
                var devname = result[1];
                var fname = result[2];
                console.log("Found annote anchor: " + devname + " " + fname);
                CTRL.registerAnnoteAnchor(devname, fname);
            }
        });
    },

    getElementsByAnnoteTuple: function (devname, fname) {
        var els = [];
        var annotes = Array.prototype.slice.call(document.querySelectorAll("desc"));
        annotes.forEach(function (annote) {
            var result = /annote=(.*),(.*)/.exec(annote.textContent);
            if (result && result[1] == devname && result[2] == fname) {
                els.push(annote.parentNode);
            }
        });
        return els;
    },

    getElementsByDeviceName: function (devname) {
        var els = [];
        var descs =  Array.prototype.slice.call(document.querySelectorAll("desc"));
        descs.forEach(function (desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if (result && result[1] == devname) {
                els.push(desc.parentNode);
            }
        });
        return els;
    },

    findParentDevice: function (el) {
        while (el) {
            var devname = Stuff.getDeviceName(el);
            if (devname)
                return devname;
            el = el.parentNode;
        }
        return null;
    },

    getDeviceName: function (el) {
        var desc = el.querySelector("desc");
        if (desc) {
            var result = /device=(.*)/.exec(desc.textContent);
            if (result)
                return result[1];
        }
        return null;
    },

    toggle: function (evt) {
        evt.stopPropagation();
        var target = evt.currentTarget;  // makes sure we get <g> element if the onclick is on it
        var devname = Stuff.findParentDevice(target);
        console.log("toggle", devname);
        if (devname)
            TANGO.toggle(devname);
        else
            console.log("no device for element " + target.getAttribute("id"));
        return false;
    },

    // create a rect for top notation
    getTopRectFromElement: function (elm) {
        var bb = elm.getBBox();
        var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("width", 10);
        rect.setAttribute("height", 5);
        rect.setAttribute("x", bb.x + bb.width * 0.5 - 5.0);
        rect.setAttribute("y", bb.y + 5 + 1);
        rect.setAttribute("style",
            "fill:#EEEEEC;stroke:orange;fill-opacity:0.5;stroke-opacity:0.7;stroke-width:0.5;");
        return rect;
    },

    getBBoxAsRectElement: function (elm){
        var bb = elm.getBBox();
        var rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        console.log("bbrect " + bb.width + ", " + bb.height);
        var padding = 0.2 * Math.min(bb.width, bb.height);
        rect.setAttribute("width", bb.width + 1.0 * padding);
        rect.setAttribute("height", bb.height + 1.0 * padding);
        rect.setAttribute("x", bb.x - padding);
        rect.setAttribute("y", bb.y - padding);
        rect.setAttribute("rx", 1.0 * padding);
        rect.setAttribute("ry", 1.0 * padding);
        rect.setAttribute("class", "select");
        return rect;
    },

    removeElementsOfClass: function (cls) {
        var els = Array.prototype.slice.call(
            document.getElementsByClassName(cls));
        els.forEach(function (el) {
            el.classList.remove(cls);
        });
    },

    hover: function (devname) {
        console.log("Hover: " + devname);
        Ui.removeElementsOfClass("hover");
        var elements = Ui.getElementsByDeviceName(devname);
        elements.forEach(function (el) {
            el.parentNode.classList.add('hover');
        });
    },

    // place top rect
    addTopRect: function (devname) {
        var elements = Ui.getElementsByDeviceName(devname);
        elements.forEach(function (el) {
            console.log("Add top rect for " + devname);
            var rect = Ui.getTopRectFromElement(el);
            el.parentNode.insertBefore(rect, el);
        });
    },

    select: function (devname) {
        console.log("Select", devname);
        var elements = Ui.getElementsByDeviceName(devname);
        Ui.removeElementsOfClass("select");

        elements.forEach(function (el) {
            //el.style.filter="url(#outline)";
            el.classList.add("select");
            //var bbrect = Ui.getBBoxAsRectElement(el);
            //el.parentNode.insertBefore(bbrect, el);
        });
    },

    setStatus: function (devname, status) {
        console.log("setStatus " + devname + " " + status);
        var els = Ui.getElementsByDeviceName(devname);
        els.forEach(function (el) {
            console.log("id: " + el.getAttribute("id"));
            el.setAttribute("class", "status-" + status);
            console.log(el.getAttribute("class"));
        });
        // set status
    },

    // put value to defined anchor
    updateData: function (rd, sp, devname, fname) {
        console.log(
            "updateData " + rd + " " + sp + " for " + devname + " [" + fname + "]");
        var elems = Ui.getElementsByAnnoteTuple(devname, fname);
        var tspan_list = elems[0].getElementsByTagName('tspan');
        if (tspan_list.length >= 1) {
            t = tspan_list[0];
            t.textContent = rd.toFixed(4) + " [" + sp.toFixed(4) + "]";
        }
    },

    updateData1: function (rd, devname, fname) {
        console.log(
            "updateData " + rd + " for " + devname + " [" + fname + "]");
        var elems = Ui.getElementsByAnnoteTuple(devname, fname);
        var tspan_list = elems[0].getElementsByTagName('tspan');
        if (tspan_list.length >= 1) {
            t = tspan_list[0];
            t.textContent = rd.toFixed(4);
        }
    }
};
