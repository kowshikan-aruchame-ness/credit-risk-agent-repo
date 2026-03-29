import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { RiskService } from './risk.service';
import { ChangeDetectorRef } from '@angular/core';


@Component({
  selector: 'app-root',
  imports: [RouterOutlet, CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  company = '';
  result: any = null;
  newsList: string[] = [];
  loading = false;
  errorMessage: string | null = null;

  constructor(private riskService: RiskService, private cdr: ChangeDetectorRef) {}

  analyze() {
    if (!this.company) return;

    this.loading = true;
    this.errorMessage = null;

    this.riskService.analyze(this.company).subscribe({
      next: (res: any) => {
        this.result = res;
        console.log(this.result);
        this.newsList = res.news_data.split('\n');
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error(err);
        this.errorMessage = 'Failed to analyze company. Please try again.';
        this.loading = false;
        this.cdr.detectChanges();
      }
    });
  }
}
