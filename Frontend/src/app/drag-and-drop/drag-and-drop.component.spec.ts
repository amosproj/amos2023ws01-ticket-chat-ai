import { TestBed, async } from '@angular/core/testing';
import { DragAndDropComponent } from './drag-and-drop.component';

describe('DragAndDropComponent', () => {
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [
        DragAndDropComponent
      ],
    }).compileComponents();
  }));

  it('should create the app', () => {
    const fixture = TestBed.createComponent(DragAndDropComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'dnd'`, () => {
    const fixture = TestBed.createComponent(DragAndDropComponent);
    const app = fixture.debugElement.componentInstance;
    expect(app.title).toEqual('dnd');
  });

  it('should render title', () => {
    const fixture = TestBed.createComponent(DragAndDropComponent);
    fixture.detectChanges();
    const compiled = fixture.debugElement.nativeElement;
    expect(compiled.querySelector('.content span').textContent).toContain('dnd app is running!');
  });
});