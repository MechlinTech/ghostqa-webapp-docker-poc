
                    describe('TestClockSessionApp', () => {
                        
        beforeEach(() => {
            cy.visit("https://www.saucedemo.com/v1/");
        });
    
                        
                        it('should execute test steps', () => {
                            
                            
                            cy.get("input#user-name").type('standard_user');
cy.get("input#password").type('secret_sauce');
cy.get("input#login-button").click();
                        });
                    });
                