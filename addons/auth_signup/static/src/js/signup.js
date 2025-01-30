/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignUpForm = publicWidget.Widget.extend({
    selector: '.oe_signup_form',
    events: {
        'submit': '_onSubmit',
        'click #togglePassword': '_togglePassword',
        'click #toggleConfirmPassword': '_toggleConfirmPassword',
    },

    //--------------------------------------------------------------------------
    // Handlers
    //--------------------------------------------------------------------------

    /**
     * @private
     */
    _onSubmit: function () {
        var $btn = this.$('.oe_login_buttons > button[type="submit"]');
        $btn.attr('disabled', 'disabled');
        $btn.prepend('<i class="fa fa-refresh fa-spin"/> ');
    },

    _togglePassword: function () {
        const passwordInput = this.$('#password');
        const eyeIcon = this.$('#eyeIcon');
        
        const inputType = passwordInput.attr('type') === 'password' ? 'text' : 'password';
        
        passwordInput.attr('type', inputType);
        if (inputType === 'password') {
            eyeIcon.removeClass('fa fa-eye-slash');
            eyeIcon.addClass('fa fa-eye');
        } else {
            eyeIcon.removeClass('fa fa-eye');
            eyeIcon.addClass('fa fa-eye-slash');
        }
    },
    
    _toggleConfirmPassword: function () {
        const confirmPasswordInput = this.$('#confirm_password');
        const confirmEyeIcon = this.$('#confirmEyeIcon');
        
        const inputType = confirmPasswordInput.attr('type') === 'password' ? 'text' : 'password';
        
        confirmPasswordInput.attr('type', inputType);
        if (inputType === 'password') {
            confirmEyeIcon.removeClass('fa fa-eye-slash');
            confirmEyeIcon.addClass('fa fa-eye');
        } else {
            confirmEyeIcon.removeClass('fa fa-eye');
            confirmEyeIcon.addClass('fa fa-eye-slash');
        }
    },
});
