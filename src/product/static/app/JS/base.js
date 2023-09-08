let sql_2 = window.matchMedia("(min-width: 767px)");

let imgLanding = document.querySelector('.images-landing img');
let paragraph = document.querySelector('.landing header .container>div:first-child p');
let logo = document.querySelector(".landing header h2");


if (imgLanding && paragraph && logo) {

  let imgsArray = ['landing-page1.jpg', 'landing-page2.jpg', 'landing-page3.jpg', 'landing-page4.jpg'];
  let classArray = ['ch1', 'ch2', 'ch3', 'ch4'];
  let imgRegex = /landing-page\d{1}\.jpg/ig;

  if (sql_2.matches) {

    setInterval(() => {
      let randomNumber = Math.floor(Math.random() * imgsArray.length);
      let newImageSrc = `static/app/images/banner/${imgsArray[randomNumber]}`;

      imgLanding.src = newImageSrc;

      if (imgRegex.test(imgLanding.src)) {
        let imgName = imgLanding.src.match(imgRegex)[0];
        let imgInx = imgsArray.indexOf(imgName);

        for (let i = 0; i < classArray.length; i++) {
          logo.classList.remove(classArray[i]);
        };

        logo.classList.add(classArray[imgInx]);
        paragraph.classList.add(classArray[imgInx]);
      };

    }, 5000);
  };

};


let sql_1 = window.matchMedia("(max-width: 766px)");

let openNav = document.querySelector('header .container nav > ul > div');

openNav.onclick = function openNav() {
  if (sql_1.matches) {
    document.getElementById('sidenav').style.width = '87%';
  }
  if (sql_2.matches) {
    document.getElementById('sidenav').style.width = '45%';
  };

  document.body.style.backgroundColor = "rgb(0 0 0 / 15%)";
};

sql_1.addListener(openNav);
sql_2.addListener(openNav);


function closeNav() {
  document.getElementById('sidenav').style.width = '0%';

  document.body.style.backgroundColor = "white";
};


let dropdownCollection = document.getElementsByClassName('dropdown_one');
for (let i = 0; i < dropdownCollection.length; i++) {
  dropdownCollection[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var dropdownContent = document.getElementsByClassName("mega-menu")[0];
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
};

let dropdownCompany = document.getElementsByClassName("dropdown_two");
for (let i = 0; i < dropdownCompany.length; i++) {
  dropdownCompany[i].addEventListener("click", function () {
    this.classList.toggle("active");
    var dropdownContent = document.getElementsByClassName("info-company")[0];
    if (dropdownContent.style.display === "block") {
      dropdownContent.style.display = "none";
    } else {
      dropdownContent.style.display = "block";
    }
  });
};



let minusCartButtons = document.querySelectorAll('.minus-cart');
let plusCartButtons = document.querySelectorAll('.plus-cart');
let removeCartButtons = document.querySelectorAll('.remove-cart');

minusCartButtons.forEach(function (minusCart) {
  minusCart.addEventListener('click', function () {
    var id = this.getAttribute('pid').toString();
    var quantElement = this.parentNode.querySelector('.quantity');

    fetch('/minus_cart?product_id=' + id, {
      method: 'GET'
    })
      .then(function (response) {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Response was not ok.');
      })
      .then(function (data) {
        quantElement.innerText = data.quantity;
        document.getElementById('amount').innerText = data.amount;
        document.getElementById('totalamount').innerText = data.totalamount;
      })
      .catch(function (error) {
        console.error('Error:', error);
      });
  });
});

plusCartButtons.forEach(function (plusCart) {
  plusCart.addEventListener('click', function () {
    var id = this.getAttribute('pid').toString();
    var quantElement = this.parentNode.querySelector('.quantity');

    fetch('/plus_cart?product_id=' + id, {
      method: 'GET'
    })
      .then(function (response) {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Response was not ok.');
      })
      .then(function (data) {
        quantElement.innerText = data.quantity;
        document.getElementById('amount').innerText = data.amount;
        document.getElementById('totalamount').innerText = data.totalamount;
      })
      .catch(function (error) {
        console.error('Error:', error);
      });
  });
});

removeCartButtons.forEach(function (removeCart) {
  removeCart.addEventListener('click', function () {
    var id = this.getAttribute('pid').toString();
    var cartInfo = this;
    fetch('/remove_cart?product_id=' + id, {
      method: 'GET'
    })
      .then(function (response) {
        if (response.ok) {
          return response.json();
        }
        throw new Error('Response was not ok.');
      })
      .then(function (data) {
        document.getElementById('amount').innerText = data.amount;
        document.getElementById('totalamount').innerText = data.totalamount;

        cartInfo.parentNode.parentNode.parentNode.remove();

        let contentCart = document.querySelector('.cart-content');
        let childCart = contentCart.children;

        if (childCart.length < 1) window.location.reload();
      })
      .catch(function (error) {
        console.error('Error:', error);
      });
  });
});



let modalImage = document.getElementById("modal-image");
function openModel(imageUrl) {
  let modal = document.getElementById("modal");
  modal.style.display = "block";
  modalImage.src = imageUrl;
}
function openSlideImage(img) {
  modalImage.src = img;
};
function closeModel() {
  var modal = document.getElementById("modal");
  modal.style.display = "none";
}


document.addEventListener('DOMContentLoaded', function () {
  const wishlistButtons = document.querySelectorAll('.wishlist-btn');

  const wishlistData = JSON.parse(localStorage.getItem('userWishlist')) || {};

  wishlistButtons.forEach(function (button) {
    const productId = button.getAttribute('pid');
    if (wishlistData[productId]) {
      button.classList.remove('plus-wishlist');
      button.classList.add('minus-wishlist');
    }
  });

  wishlistButtons.forEach(function (button) {
    button.addEventListener('click', function (event) {
      event.preventDefault();
      const productId = button.getAttribute('pid');
      const isAdding = button.classList.contains('plus-wishlist');

      fetch(isAdding ? `/add_to_wishlist/?product_id=${productId}` : `/remove_from_wishlist/?product_id=${productId}`)
        .then(response => {
          if (response.ok) {
            return response.json();
          }
          throw new Error('Response was not ok.');
        })
        .then(data => {
          if (isAdding) {
            button.classList.remove('plus-wishlist');
            button.classList.add('minus-wishlist');
            wishlistData[productId] = true;
          } else {
            button.classList.remove('minus-wishlist');
            button.classList.add('plus-wishlist');
            delete wishlistData[productId];
          }

          localStorage.setItem('userWishlist', JSON.stringify(wishlistData));

          window.location.reload();
        })
        .catch(error => {
          console.error('Error:', error);
        });
    });
  });
});


let upScroll = document.getElementById('up-scroll');
window.onscroll = function () {
  if (window.scrollY >= 700) upScroll.style.opacity = '1';
  else upScroll.style.opacity = '0';
};

upScroll.onclick = function () {
  window.scrollTo({
    top: 0,
    behavior: 'smooth',
  })
};


id_show_password.onclick = togglePassword;
function togglePassword() {
  if (id_show_password.checked) {
    id_password.type = 'text';
  } else {
    id_password.type = 'password';
  };
};