import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';
import { HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('AppComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [
        RouterTestingModule,
        HttpClientModule,
        MatFormFieldModule,
        FormsModule,
        MatInputModule,
        BrowserAnimationsModule
      ],
      declarations: [AppComponent]
    }).compileComponents();
  });

  it('should create the app', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'TalkTix'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual('TalkTix');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(AppComponent);
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    expect(compiled.querySelector('h1')?.textContent).toContain('TalkTix');
  });

  // doesnt work 100% correctly, just initial, after that it lose connection, which it should not do
  it('should display user message and server response correctly', () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    const testMessage = 'Testnachricht';
  
    // set the chat input
    app.chatInput = testMessage;
  
    // call handleSend directly without simulating button click
    app.handleSend(testMessage);
  
    // check if user message is displayed correctly
    expect(app.chatMessages[app.chatMessages.length - 1]).toEqual({ messageText: testMessage, isUser: true });
  
    // simulate server response
    const serverResponse = 'Serverantwort';
    app.chatMessages.push({ messageText: serverResponse, isUser: false });
  
    // check if server response is displayed correctly
    expect(app.chatMessages[app.chatMessages.length - 1]).toEqual({ messageText: serverResponse, isUser: false });
  });
