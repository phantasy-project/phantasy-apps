var Ui = {

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
            }
        });
        CTRL.loadDeviceDone();
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
            document.getElementsByClassName("select"));
        els.forEach(function (el) {
            el.parentNode.removeChild(el);
        });
    },

//    hover: function (devname) {
//        console.log("Hover", devname);
//        var elements = Ui.getElementsByDeviceName(devname);
//        
//        elements.forEach(function (el) {
//            el.parentNode.setAttribute('title', devname);
//        });
//    },

    select: function (devname) {
        console.log("Select", devname);
        var elements = Ui.getElementsByDeviceName(devname);
        Ui.removeElementsOfClass("select");

        elements.forEach(function (el) {
            //el.style.filter="url(#outline)";
            var bbrect = Ui.getBBoxAsRectElement(el);
            el.parentNode.insertBefore(bbrect, el);
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
    }

};
