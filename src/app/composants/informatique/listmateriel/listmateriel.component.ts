import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'wae-listmateriel',
  templateUrl: './listmateriel.component.html',
  styleUrls: ['./listmateriel.component.css']
})
export class ListmaterielComponent implements OnInit {
  materiels = [
    {
      id: '1',
      libelle: 'Ecran',
      photo: 'assets/Images/Informatique/ecran.png',
      marque: 'LG',
      prix: 400.3,
      description: 'Ecran de dernière génération',
      hautGamme: true,
      quantite: 10,
      commentaires: [{ contenu: ' satisfaisant', note: 3, auteur: 'Sami MRAD', date: new Date(2020, 11, 4) },
      { contenu: 'Bon rapport qualité prix', note: 4, auteur: 'Amira Salah', date: new Date(2020, 10, 4) }]
    },
    {
      id: '2',
      libelle: 'PC',
      photo: 'assets/Images/Informatique/pcFixe.jpg',
      marque: 'HP',
      prix: 1780.6,
      description: 'PC Portable très pratique',
      hautGamme: false,
      quantite: 5,
      commentaires: [{ contenu: ' satisfaisant', note: 3, auteur: 'Sami MRAD', date: new Date(2020, 11, 4) },
      { contenu: 'Bon rapport qualité prix', note: 4, auteur: 'Samar Salah', date: new Date(2020, 10, 4) }]
    },
    {
      id: '3',
      libelle: 'Scanner',
      photo: 'assets/Images/Informatique/scanner.jpg',
      marque: 'HP',
      prix: 380.5,
      description: 'Scanner Ultra rapide',
      hautGamme: true,
      quantite: 0,
      commentaires: []
    },
    {
      id: '4',
      libelle: 'Imprimante',
      photo: '../assets/Images/Informatique/imprimante.jpg',
      marque: 'Canon',
      prix: 420,
      description: 'Imprimante multifonctions avec kit',
      hautGamme: false,
      quantite: 1,
      commentaires: []
    },
    {
      id: '5',
      libelle: 'PC Portable',
      photo: '../assets/Images/Informatique/pcPortable.png',
      marque: 'Dell',
      prix: 2250,
      description: 'PC Portable très performant',
      hautGamme: true,
      quantite: 2,
      commentaires: []
    }

  ];

  constructor() { }

  ngOnInit(): void {
  }

}
