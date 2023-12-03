import { TestBed, ComponentFixture, inject } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatCardModule } from '@angular/material/card';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { of } from 'rxjs';
import { TicketService } from './service/ticket.service'; // Update the path
import { DragAndDropComponent } from './drag-and-drop/drag-and-drop.component';

describe('AppComponent', () => {
  let fixture: ComponentFixture<AppComponent>;
  let app: AppComponent;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientModule,
        MatFormFieldModule,
        FormsModule,
        MatInputModule,
        MatCardModule,
        BrowserAnimationsModule
      ],
      declarations: [
        AppComponent,
        DragAndDropComponent
      ],
      providers: [
        // Add the TicketService to the providers array
        TicketService,
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    app = fixture.componentInstance;
  });

  it('should create the app', () => {
    expect(app).toBeTruthy();
  });

  it(`should have as title 'TalkTix'`, () => {
    expect(app.title).toEqual("TalkTix");
  });

  it('should render title', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('TalkTix');
  });

  it('should display user message and server response correctly', inject([TicketService], (ticketService: TicketService) => {
    const testMessage = 'Testnachricht';
    const emailInput = 'test@example.com';

    // set the chat input and emailInput
    app.chatInput = testMessage;

    // spy on the send method of TicketService
    spyOn(ticketService, 'send').and.returnValue(of('Serverantwort'));

    // call handleSend
    app.handleSend(testMessage, emailInput);

    // check if user message is displayed correctly
    expect(app.chatMessages[app.chatMessages.length - 2]).toEqual({ messageText: testMessage, isUser: true, files: [] });

    // check if server response is displayed correctly
    expect(app.chatMessages[app.chatMessages.length - 1]).toEqual({ messageText: '"Serverantwort"', isUser: false, files: [] });

    // check if the send method was called with the correct arguments
    expect(ticketService.send).toHaveBeenCalledWith(testMessage, emailInput);
  }));

  // Add more tests as needed for the updated functionality
});
