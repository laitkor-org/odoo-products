let accordionProductFields = document.getElementsByClassName("accordionProductFields");

for (let i = 0; i < accordionProductFields.length; i++) {
    accordionProductFields[i].addEventListener("click", function () {
        this.classList.toggle("activeProductField");
        let panel = this.nextElementSibling;
        
        document.querySelectorAll('.panelProductFields').forEach(p => {
            p.style.maxHeight = null;
            p.style.padding = "0px";
        });

        document.querySelectorAll('.accordionProductFields').forEach(btn => btn.classList.remove("activeProductField"));

        if (!panel.style.maxHeight) {
            this.classList.add("activeProductField");
            panel.style.maxHeight = (panel.scrollHeight + 20) + "px"; // Adding padding offset
            panel.style.padding = "10px 15px";
        }
    });
}