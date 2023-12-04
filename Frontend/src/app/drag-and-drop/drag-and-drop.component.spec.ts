import { TestBed, async, ComponentFixture } from '@angular/core/testing';
import { Component } from '@angular/core';
import { By } from '@angular/platform-browser';
import { DndDirective } from './directive/dnd.directive';

@Component({
  template: `
    <div class="container" appDnd (fileDropped)="onFileDropped($event)"></div>
  `,
})
class TestHostComponent {
  onFileDropped(event: any) {}
}

describe('DndDirective', () => {
  let fixture: ComponentFixture<TestHostComponent>;
  let hostComponent: TestHostComponent;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DndDirective, TestHostComponent],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TestHostComponent);
    hostComponent = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the directive', () => {
    const directive = fixture.debugElement.query(By.directive(DndDirective));
    expect(directive).toBeTruthy();
  });

  it('should trigger dragover event', () => {
    const divElement = fixture.debugElement.query(By.css('.container'));
    const dragoverEvent = createEvent('dragover');
    fixture.detectChanges();
    divElement.triggerEventHandler('dragover', dragoverEvent);
    fixture.detectChanges();
  
    expect(divElement.classes['fileOver']).toBe(true);
  });  
  /*
  it('should trigger dragleave event', (done) => {
    const divElement = fixture.debugElement.query(By.css('.container'));
    const dragleaveEvent = createEvent('dragleave');
    divElement.triggerEventHandler('dragleave', dragleaveEvent);
    fixture.detectChanges();
  
    setTimeout(() => {
      expect(divElement.classes['fileOver']).toBe(false);
      done();
    }, 100); // Adjust the timeout as needed
  });
  

  it('should trigger drop event', () => {
    const divElement = fixture.debugElement.query(By.css('.container'));
    const dropEvent = createEvent('drop', { files: ['test.txt'] });
    spyOn(hostComponent, 'onFileDropped');

    // Update: Trigger the 'drop' event on the divElement
    divElement.triggerEventHandler('drop', dropEvent);

    expect(divElement.classes['fileOver']).toBe(false);
    expect(hostComponent.onFileDropped).toHaveBeenCalledWith(['test.txt']);
  });
  */
  function createEvent(type: string, data?: any): Event {
    const event: any = new Event(type);
    event.dataTransfer = { files: data ? data.files : [] };
    return event;
  }
});
