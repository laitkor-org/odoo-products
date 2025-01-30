/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.portalDetails = publicWidget.Widget.extend({
    selector: '.o_portal_details',
    events: {
        'change select[name="country_id"]': '_onCountryChange',
        'input .zipInput':'_onPincodeChange',
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this.$state = this.$('select[name="state_id"]');
        this.$stateOptions = this.$state.filter(':enabled').find('option:not(:first)');
        this.$zipcode = this.$('input[name="zipcode"]');
        this.$city =this.$('input[name="city"]');
        if (!this.$zipcode.length || !this.$city.length || !this.$state.length) {
            console.error("Missing required input elements: zipcode, city, or state.");
        }
        this._adaptAddressForm();
        this.$zipcode.on('input', this._onPincodeChange.bind(this));
        return def;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _adaptAddressForm: function () {
        var $country = this.$('select[name="country_id"]');
        var countryID = ($country.val() || 0);
        this.$stateOptions.detach();
        var $displayedState = this.$stateOptions.filter('[data-country_id=' + countryID + ']');
        var nb = $displayedState.appendTo(this.$state).show().length;
        this.$state.parent().toggle(nb >= 1);
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onCountryChange: function () {
        this._adaptAddressForm();
    },

    /**
     * @param {string} zipcode
     */
    _fetchCityState: function(zipcode){
        const url =`/portal/pincode_data`;
        const payload = { zipcode };

        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        })
        .then(response => response.json())
        .then(data => {
            let result= data.result;
            if (typeof result === 'string') {
                try {
                    result = JSON.parse(result);
                } catch (e) {
                    console.error('Error parsing result string:', e);
                    return;  
                }
            }
            if (result && result.error) {
                console.error('Error fetching city/state:', data.error);
                this.$city.val('');
                this.$state.val('');
            } else {
                if (result && result.length > 0) {
                    const city = result[0].City || '';
                    const stateName = result[0].State || '';
                    this.$city.val(city);
                    const $matchstate = this.$state.find(`option`).filter(function(){
                       return $(this).text().trim() === stateName.trim();
                    });
                    if ($matchstate.length) {
                       this.$state.val($matchstate.val()); 
                    } else {
                       this.$state.val('');
                    }

                }else {
                    this.$city.val('');
                    this.$state.val('');
                }
            }
    })
         .catch((error) => {
        
             console.error('Error fetching city/state:', error);
             this.$city.val('');
             this.$state.val('');
         });
     }, 


    _onPincodeChange: function() {
        const zipcode = this.$zipcode.val();
        if (!zipcode || zipcode.trim() === '' || zipcode.length < 4){
            this.$city.val('');
            this.$state.val('');
          
        } else{
            this._fetchCityState(zipcode);
        }
    },
});

export const PortalHomeCounters = publicWidget.Widget.extend({
    selector: '.o_portal_my_home',

    init() {
        this._super(...arguments);
        this.rpc = this.bindService("rpc");
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this._updateCounters();
        return def;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * Return a list of counters name linked to a line that we want to keep
     * regardless of the number of documents present
     * @private
     * @returns {Array}
     */
    _getCountersAlwaysDisplayed() {
        return [];
    },

    /**
     * @private
     */
    async _updateCounters(elem) {
        const numberRpc = 3;
        const needed = Object.values(this.el.querySelectorAll('[data-placeholder_count]'))
                                .map(documentsCounterEl => documentsCounterEl.dataset['placeholder_count']);
        const counterByRpc = Math.ceil(needed.length / numberRpc);  // max counter, last can be less
        const countersAlwaysDisplayed = this._getCountersAlwaysDisplayed();

        const proms = [...Array(Math.min(numberRpc, needed.length)).keys()].map(async i => {
            const documentsCountersData = await this.rpc("/my/counters", {
                counters: needed.slice(i * counterByRpc, (i + 1) * counterByRpc)
            });
            Object.keys(documentsCountersData).forEach(counterName => {
                const documentsCounterEl = this.el.querySelector(`[data-placeholder_count='${counterName}']`);
                documentsCounterEl.textContent = documentsCountersData[counterName];
                if (documentsCountersData[counterName] !== 0 || countersAlwaysDisplayed.includes(counterName)) {
                    documentsCounterEl.closest('.o_portal_index_card').classList.remove('d-none');
                }
            });
            return documentsCountersData;
        });
        return Promise.all(proms).then((results) => {
            this.el.querySelector('.o_portal_doc_spinner').remove();
        });
    },
});

publicWidget.registry.PortalHomeCounters = PortalHomeCounters;

publicWidget.registry.portalSearchPanel = publicWidget.Widget.extend({
    selector: '.o_portal_search_panel',
    events: {
        'click .dropdown-item': '_onDropdownItemClick',
        'submit': '_onSubmit',
        'click #toggleCurrentPassword': '_toggleCurrentPassword',
        'click #toggleNewPassword': '_toggleNewPassword',
        'click #toggleVerifyNewPassword': '_toggleVerifyNewPassword',
    },

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this._adaptSearchLabel(this.$('.dropdown-item.active'));
        return def;
    },

    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _adaptSearchLabel: function (elem) {
        var $label = $(elem).clone();
        $label.find('span.nolabel').remove();
        this.$('input[name="search"]').attr('placeholder', $label.text().trim());
    },
    /**
     * @private
     */
    _search: function () {
        var search = new URL(window.location).searchParams;
        search.set("search_in", this.$('.dropdown-item.active').attr('href')?.replace('#', '') || "");
        search.set("search", this.$('input[name="search"]').val());
        window.location.search = search.toString();
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onDropdownItemClick: function (ev) {
        ev.preventDefault();
        var $item = $(ev.currentTarget);
        $item.closest('.dropdown-menu').find('.dropdown-item').removeClass('active');
        $item.addClass('active');
        this._adaptSearchLabel(ev.currentTarget);
    },
    /**
     * @private
     */
    _onSubmit: function (ev) {
        ev.preventDefault();
        this._search();
    },

    _toggleCurrentPassword: function () {
        const currentPasswordInput = this.$('#current');
        const currentEyeIcon = this.$('#currentEyeIcon');
        
        const inputType = currentPasswordInput.attr('type') === 'password' ? 'text' : 'password';
        
        currentPasswordInput.attr('type', inputType);
        if (inputType === 'password') {
            currentEyeIcon.removeClass('fa fa-eye-slash');
            currentEyeIcon.addClass('fa fa-eye');
        } else {
            currentEyeIcon.removeClass('fa fa-eye');
            currentEyeIcon.addClass('fa fa-eye-slash');
        }
    },
    
    _toggleNewPassword: function () {
        const newPasswordInput = this.$('#new');
        const newEyeIcon = this.$('#newEyeIcon');
        
        const inputType = newPasswordInput.attr('type') === 'password' ? 'text' : 'password';
        
        newPasswordInput.attr('type', inputType);
        if (inputType === 'password') {
            newEyeIcon.removeClass('fa fa-eye-slash');
            newEyeIcon.addClass('fa fa-eye');
        } else {
            newEyeIcon.removeClass('fa fa-eye');
            newEyeIcon.addClass('fa fa-eye-slash');
        }
    },
    
    _toggleVerifyNewPassword: function () {
        const verifyNewPasswordInput = this.$('#new2');
        const verifyNewEyeIcon = this.$('#verifyNewEyeIcon');
        
        const inputType = verifyNewPasswordInput.attr('type') === 'password' ? 'text' : 'password';
        
        verifyNewPasswordInput.attr('type', inputType);
        if (inputType === 'password') {
            verifyNewEyeIcon.removeClass('fa fa-eye-slash');
            verifyNewEyeIcon.addClass('fa fa-eye');
        } else {
            verifyNewEyeIcon.removeClass('fa fa-eye');
            verifyNewEyeIcon.addClass('fa fa-eye-slash');
        }
    }
});
