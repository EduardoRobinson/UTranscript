import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { IonicModule } from '@ionic/angular';

import { ReadByIdPageRoutingModule } from './read-by-id-routing.module';

import { ReadByIdPage } from './read-by-id.page';

@NgModule({
  imports: [
    CommonModule,
    FormsModule,
    IonicModule,
    ReadByIdPageRoutingModule
  ],
  declarations: [ReadByIdPage]
})
export class ReadByIdPageModule {}
