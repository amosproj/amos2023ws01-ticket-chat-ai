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
import { MatDialogModule } from "@angular/material/dialog";

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
        BrowserAnimationsModule,
        MatDialogModule
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

    // check if the send method was called with the correct arguments
    expect(ticketService.send).toHaveBeenCalledWith(testMessage, emailInput);
  }));

  it('should display the correct text on the recording button depending on state', async () => {

    const recordButton = fixture.debugElement.nativeElement.querySelector('.record-button');

    recordButton.click();
    fixture.detectChanges();
    expect(recordButton.textContent.trim()).toEqual('Stop recording speech');

    recordButton.click();
    fixture.detectChanges();
    expect(recordButton.textContent.trim()).toEqual('Start recording speech');

  })

  it('should call the right method after click the recording button', () => {
    const startRecordingSpy = spyOn(app, 'startRecording');

    const recordButton = fixture.debugElement.nativeElement.querySelector('.record-button');

    recordButton.click();
    expect(startRecordingSpy).toHaveBeenCalledWith();
  })

  it('should call the right method after click the recording button twice', () => {
    const stopRecordingSpy = spyOn(app, 'stopRecording');

    const recordButton = fixture.debugElement.nativeElement.querySelector('.record-button');

    recordButton.click();
    recordButton.click();

    expect(stopRecordingSpy).toHaveBeenCalledWith();
  })

  // Add more tests as needed for the updated functionality
});
