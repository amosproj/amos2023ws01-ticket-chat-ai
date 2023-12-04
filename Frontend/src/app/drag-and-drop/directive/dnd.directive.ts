import {
    Directive,
    Output,
    Input,
    EventEmitter,
    HostBinding,
    HostListener
  } from '@angular/core';
  
  @Directive({
    selector: '[appDnd]'
  })
  export class DndDirective {
    @HostBinding('class.fileOver') fileOver: boolean | undefined;
    @Output() fileDropped = new EventEmitter<any>();
  
    // Dragover listener
    @HostListener('dragover', ['$event']) onDragOver(evt: any) {
      evt.preventDefault();
      evt.stopPropagation();
      this.fileOver = true;
    }
  
    @HostListener('dragleave', ['$event']) public onDragLeave(evt: any) {
      evt.preventDefault();
      evt.stopPropagation();
      console.log('Drag leave event triggered');
      this.fileOver = false;
      console.log('fileOver:', this.fileOver);
    }
  
    // Drop listener
    @HostListener('drop', ['$event']) public ondrop(evt: any) {
      evt.preventDefault();
      evt.stopPropagation();
      this.fileOver = false;
      let files = evt.dataTransfer.files;
      if (files.length > 0) {
        this.fileDropped.emit(files);
      }
    }
  }