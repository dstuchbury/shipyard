FROM php:8.2-fpm

ARG UID=1000
ARG GID=1000
ARG USER=www

RUN apt-get update && apt-get install -y \
    mariadb-client \
    libpng-dev \
    libxml2-dev \
    dnsutils \
    libxrender1 \
    libjpeg62-turbo-dev \
    libfreetype6-dev \
    locales \
    unzip \
    curl \
    libzip-dev \
    libonig-dev \
    ghostscript \
    libmagickwand-dev \
    git \
    zip \
    vim \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN docker-php-ext-install pdo_mysql mbstring zip exif pcntl xml soap
RUN docker-php-ext-configure gd --with-freetype --with-jpeg
RUN docker-php-ext-install gd

COPY --from=composer:2 /usr/bin/composer /usr/local/bin/composer

#COPY .docker/php/conf/local.ini /usr/local/etc/php/conf.d/local.ini
#RUN rm /usr/local/etc/php-fpm.d/www.conf
#COPY .docker/php/conf/www.conf /usr/local/etc/php-fpm.d/www.conf

RUN groupadd -g ${GID} ${USER} \
    && useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER}

ENV HOME=/home/${USER}
ENV XDG_CONFIG_HOME=/home/${USER}/.config
ENV XDG_DATA_HOME=/home/${USER}/.local/share
ENV COMPOSER_HOME=/home/${USER}/.composer

RUN mkdir -p ${XDG_CONFIG_HOME} ${XDG_DATA_HOME} ${COMPOSER_HOME} \
    && chown -R ${UID}:${GID} /home/${USER}

WORKDIR /var/www/html

USER ${USER}

EXPOSE 9000
CMD ["php-fpm"]
