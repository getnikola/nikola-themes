all: prd

dev:
	sass --style expanded --line-numbers --load-path ../material-design-lite/src sass/styles.scss assets/css/styles.css
ifneq ($(wildcard sass/custom.scss),)
	sass --style expanded --line-numbers sass/custom.scss assets/css/custom.css
endif

prd:
	sass --style compressed --load-path ../material-design-lite/src sass/styles.scss assets/css/styles.css
ifneq ($(wildcard sass/custom.scss),)
	sass --style compressed sass/custom.scss assets/css/custom.css
endif

colorbox:
	cd ./assets/vendor/colorbox/css/ && uglifycss colorbox.css > colorbox.min.css
