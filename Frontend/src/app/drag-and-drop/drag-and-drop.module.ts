import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { ProgressComponent } from './components/progress/progress.component';
import { DragAndDropComponent } from './drag-and-drop.component';
import { DndDirective } from './directive/dnd.directive';

@NgModule({
  declarations: [
    DragAndDropComponent,
    DndDirective,
    ProgressComponent
  ],
  imports: [
    BrowserModule
  ]
})
export class DragAndDropModule { }