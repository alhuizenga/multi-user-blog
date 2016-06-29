from functools import wraps


def user_required(path='/user/login'):
    def validate_user(func):
        @wraps(func)
        def validate(self):
            print "validating..."
            # make sure we are logged in right meow
            # validate the cookie itself, since we need to be sure
            # they are who they say they are
            if not self.validate_sig():
                self.invalidate_sig()
                self.redirect(path)
                return func(self, None)
            user = self.retrieve_sig_data()

            sess_user = self.session.get('user')
            if sess_user is None:
                self.invalidate_sig()
                self.redirect(path)
                return func(self, None)
            if user != sess_user:
                # the user is not who they say they are
                self.invalidate_sig()
                self.redirect(path)
                return func(self, None)
            return func(self, user)
        return validate
    return validate_user