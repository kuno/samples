intainer: Your Name <youremail at domain dot com>

pkgname=NAME
pkgver=VERSION
pkgrel=1
pkgdesc=""
arch=('i686' 'x86_64')
url="http://ADDRESS/"
license=('GPL')
groups=()
depends=()
makedepends=()
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
source=($pkgname-$pkgver.tar.gz)
noextract=()
md5sums=() #generate with 'makepkg -g'

build() {
      cd $srcdir/$pkgname-$pkgver
        ./configure --prefix=/usr
	  make || return 1
	    make DESTDIR=$pkgdir install || return 1
}
