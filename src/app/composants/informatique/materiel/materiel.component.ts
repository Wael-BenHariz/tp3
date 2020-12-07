import { Component, Input, OnInit } from '@angular/core';
import { Materiel } from 'src/app/models/materiel';

@Component({
  selector: 'wae-materiel',
  templateUrl: './materiel.component.html',
  styleUrls: ['./materiel.component.css']
})
export class MaterielComponent implements OnInit {
 // tslint:disable-next-line: no-input-rename
 @Input('m') t: Materiel;
  constructor() { }

  ngOnInit(): void {
  }

}
