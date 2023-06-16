import { MediaMatcher } from '@angular/cdk/layout';
import { Injectable, NgZone } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({
    providedIn: 'root',
})
export class MediaService {

    private readonly mobileWidthBreakpoint: number = 960; // px

    private _isMobile: boolean;
    public get isMobile(): boolean { return this._isMobile; }

    private mobileMedia$: BehaviorSubject<boolean>;
    public get mobileMediaChange(): Observable<boolean> { return this.mobileMedia$.asObservable(); }

    constructor(
        private mediaMatcher: MediaMatcher,
        private ngZone: NgZone,
    ) {
        const mediaMatch = this.mediaMatcher.matchMedia(`(max-width: ${this.mobileWidthBreakpoint}px)`);

        this._isMobile = mediaMatch.matches;
        if (this._isMobile == null) {
            this._isMobile = window.innerWidth <= this.mobileWidthBreakpoint;
        }
        this.mobileMedia$ = new BehaviorSubject<boolean>(this.isMobile);

        (mediaMatch as any).onchange = (e: any) => this.ngZone.run(() => {
            this._isMobile = e.matches;
            this.mobileMedia$.next(this.isMobile);
        });
    }
}
