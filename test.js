describe('monuTest', () => {

    beforeEach(() => {
        cy.visit("https://google.com");
    });


                    it('should execute test steps', () => {


                        cy.get("['data-test=new-todo']").type('Feed the cat');
                    });
                });


                describe('todoAppTests', () => {

    beforeEach(() => {
        cy.visit("https://example.cypress.io/todo");
    });


                    it('should execute test steps', () => {
                        cy.visit('https://example.cypress.io/todo');

                        cy.visit("https://google.com");
cy.get(".todo-list li").should('include.text', 'Pay electric bill');
cy.get(".todo-list li").should('include.text', 'Walk the dog');
cy.get("['data-test=new-todo']").type('Feed the cat');
cy.get('body').type('Enter');
cy.get(".todo-list li").should('include.text', 'Feed the cat');
cy.get(".todo-list li:nth-child(1) input[type=checkbox]").check();
cy.get(".todo-list li:nth-child(1)").should('have.class', 'completed');
cy.get(":contains('Active')").click();
cy.get(".todo-list li").should('include.text', 'Walk the dog');
cy.get(":contains('Pay electric bill')").should('not.exist');
cy.get(":contains('Completed')").click();
cy.get(".todo-list li").should('include.text', 'Pay electric bill');
cy.get(":contains('Walk the dog')").should('not.exist');
cy.get(":contains('Clear completed')").click();
cy.get(".todo-list li").should('have.length', 1);

cy.get(":contains('Clear completed')").should('not.exist');
                    });
                });


                describe('googleSearch', () => {


                    it('should execute test steps', () => {
                        cy.visit('https://www.google.com');

                        cy.get("input[name='q']").type('Cypress E2E testing');
cy.get('body').type('Enter');
cy.wait(2000);
cy.get("None").should('include.text', 'Cypress E2E testing');
                    });
                });


                describe('test1', () => {


                    it('should execute test steps', () => {
                        cy.visit('/path/to/test1');

                        cy.visit("/path/to/test1");
cy.get("button#login-btn").click();
cy.get("input#username").type('testuser');
cy.get("input#password").type('testpassword');
cy.get('body').type('Enter');
cy.wait(2000);
cy.get('body').scrollDown(300);
cy.get("a#hover-element").trigger('mouseover');
cy.get("div#success-message").should('exist');
                    });
                });


                describe('test2', () => {


                    it('should execute test steps', () => {
                        cy.visit('/path/to/test2');

                        cy.visit("/path/to/test2");
cy.get("button#load-data-btn").click();
cy.wait(1000);
cy.get("select#data-dropdown").select('Option 1');
cy.get("input#agree-checkbox").check();
cy.get("input#disagree-checkbox").uncheck();
cy.get("div#result").should('include.text', 'Data loaded successfully');
                    });
                });